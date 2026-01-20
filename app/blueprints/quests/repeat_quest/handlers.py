from flask import Request
from datetime import datetime, timezone
import random

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.enums import QuestState, QuestTitle
from app.models import User
from app.authentication_manager import authenticator
from app.errors import QuestError, GameError


def get_handlers():
    return {"GET": get_handler, "POST": post_handler}


def get_quest_vars() -> (int, int, int):
    return (20, 3, 10)  # total, min, max


def get_handler(quest: QuestData, req: Request):
    username = parser_utils.get_auth_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.BEG_QUEST.value)
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    User.update_last_beg_req_at(username)
    
    target_reqs, min_wait, max_wait = get_quest_vars()
    formatting = {"HERO": username,
                  "TOTAL_REQS": target_reqs,
                  "MIN_WAIT": min_wait,
                  "MAX_WAIT": max_wait
                  }
    content = content_generator.create_content(quest, state, formatting)
    return content


def post_handler(quest: QuestData, req: Request):
    # setup
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.BEG_QUEST.value)
    
    # quest vars
    please_streak = User.get_beg_counter(username)
    target_reqs, min_wait, max_wait = get_quest_vars()
    formatting = {"HERO": username,
                  "REQ_LEFT": target_reqs - please_streak,
                  "TOTAL_REQS": target_reqs,
                  "MIN_WAIT": min_wait,
                  "MAX_WAIT": max_wait
                  }
    
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    # validate that the json input
    if jason_says_please(req) is False:
        raise QuestError("... I am quite literal when I want jason to say:please")
    
    # validate the request timing
    delta_req_time = get_delta_since_last_req(username)
    if delta_req_time < 0:
        raise GameError("Something went wrong with the request delta time and it is not on you. Talk with a TA.")
    
    if delta_req_time < min_wait or delta_req_time > max_wait:  # check if requesting too fast
        User.update_xp(username, -please_streak)
        please_streak = User.update_beg_counter(username, -please_streak)
        User.update_last_beg_req_at(username)
        resp = get_failure_response()
        raise QuestError(f"{resp}. You decided to wait {delta_req_time} seconds. {please_streak} of {target_reqs}")
    else:  # request accepted
        please_streak = User.update_beg_counter(username, 1)  # system will raise error before if not accepted
        User.update_xp(username, 1)
    
    # check if quest is completed and update content accordingly
    # assuming fail / not completed
    state = QuestState.FAILED.value
    User.update_last_beg_req_at(username)  # updating timeout
    content = content_generator.create_content(quest, state, formatting)
    content.update({"status": "trying"})
    content.update({"story": get_correct_response(please_streak, target_reqs) + f" {please_streak} of {target_reqs}"})
    if quest_completed(please_streak, target_reqs):
        state = QuestState.COMPLETED.value
        User.update_quest_state(username, QuestTitle.BEG_QUEST.value, state)
        User.update_xp(username, 10)
    return content


def jason_says_please(req: Request) -> bool:
    json = parser_utils.get_json(req)
    print(f"json: {json}")
    json_says = json.get("say", "")
    if not isinstance(json_says, str):
        raise ValueError('Expected jasons speaking to be a bit more.... "STRINGent?"')
    return json_says.lower() == "please"


def get_delta_since_last_req(username: str) -> int:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    last_attempt_at = User.get_last_beg_req_at(username)
    delta_time = (now - last_attempt_at).total_seconds() if last_attempt_at else -1
    return delta_time


def quest_completed(counter: int, target: int) -> bool:
    return counter >= target


def get_correct_response(counter: int, target: int) -> str:
    if random.random() < 0.7:
        return get_standard_success_response()
    if target/counter < 0.33:
        return get_first_correct_response()
    elif target/counter < 0.66:
        return get_middle_correct_responses()
    return get_final_winning_responses()


def get_first_correct_response():
    responses = ["This is trivial. Anyone could do this.",
                 "Dont mistake obedience for progress.",
                 "Youll slip. They always do."]
    return random.choice(responses)

    
def get_middle_correct_responses():
    responses = ["Why are you still succeeding?",
                 "This task was meant to be annoying.",
                 "Jason is saying it too cleanly.",
                 "I may need to recount.",
                 "This is taking longer than anticipated."]
    return random.choice(responses)

    
def get_final_winning_responses():
    responses = ["Stop being consistent!",
                 "That shouldn’t still be working!",
                 "I never said you were close.",
                 "The Crown is symbolic anyway.",
                 "You don’t even want it.",
                 "This is not victory. This is bureaucracy."]
    return random.choice(responses)


def get_standard_success_response():
    responses = ["Hmph. That ‘please’ was acceptable. Don’t get comfortable.",
                 "You barely respected my rules.",
                 "I said wait. You waited. Annoyingly well.",
                 "Fine. The streak continues. For now.",
                 "Jason sounded reluctant. I liked that part.",
                 "That timing was… correct. I hate that.",
                 "Again? You’re really committing to this nonsense.",
                 "Careful. One slip and I reset everything.",
                 "You didn’t rush. You didn’t delay. How dull.",
                 "Another valid ‘please.’ This is getting tiresome.",
                 "Don’t think repetition impresses me.",
                 "You’re obeying the rules too well.",
                 "Yes, yes—Jason said it properly. Moving on.",
                 "Your streak survives. Regrettably.",
                 "That pause was within bounds. I checked.",
                 "You’re treating this like a system. I resent that.",
                 "Correct again. Statistically irritating.",
                 "You’re not clever—you’re just compliant.",
                 "Keep going. I’m sure you’ll mess up eventually.",
                 "Another success. The CRUDe Crown remains just out of reach."]
    return random.choice(responses)

    
def get_failure_response():
    responses = ["OH! Too fast. Reset.",
                 "Rules are rules. Back to zero.",
                 "I warned you. I loved warning you.",
                 "Reset! Glorious, beautiful reset!",
                 "Patience failed you. Again.",
                 "All that progress? Gone.",
                 "Say it again. From the beginning.",
                 "This is why I make the rules.",
                 "MWAHAHA—compose yourself. You’ll need to start over."]
    return random.choice(responses)