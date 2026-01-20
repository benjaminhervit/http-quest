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
    return {"GET": get_handler, "POST": delete_handler}


def get_quest_vars() -> (int, int, int):
    return (20, 3, 10, "jason", "smash!")  # total, min, max, json_key, json_val


def get_handler(quest: QuestData, req: Request):
    username = parser_utils.get_auth_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.WALL_QUEST.value)
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    User.update_wall_last_req_at(username)
    
    target_reqs, min_wait, max_wait, json_key, json_val = get_quest_vars()
    formatting = {"HERO": username,
                  "TOTAL_REQS": target_reqs,
                  "MIN_WAIT": min_wait,
                  "MAX_WAIT": max_wait,
                  "JSON_KEY": json_key,
                  "JSON_VAL": json_val
                  }
    content = content_generator.create_content(quest, state, formatting)
    return content


def delete_handler(quest: QuestData, req: Request):
    # setup
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.BEG_QUEST.value)
    
    # quest vars
    hit_streak = User.get_wall_counter(username)
    target_reqs, min_wait, max_wait, json_key, json_val = get_quest_vars()
    formatting = {"HERO": username,
                  "TOTAL_REQS": target_reqs,
                  "MIN_WAIT": min_wait,
                  "MAX_WAIT": max_wait,
                  "JSON_KEY": json_key,
                  "JSON_VAL": json_val
                  }
    
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    if state == QuestState.COMPLETED.value:
        return content_generator.create_completed_content(quest)
    
    # validate that the json input
    if jason_is_smashing(req) is False:
        raise QuestError("... You need to get Jason to smash!")
    
    # validate the request timing
    delta_req_time = get_delta_since_last_req(username)
    if delta_req_time < 0:
        raise GameError("Something went wrong with the request delta time and it is not on you. Talk with a TA.")
    
    if delta_req_time < min_wait or delta_req_time > max_wait:  # check if requesting too fast
        # User.update_xp(username, -hit_streak)
        hit_streak = User.reset_wall_counter(username)
        User.update_wall_last_req_at(username)
        resp = get_failure_response()
        raise QuestError(f"{resp}. You decided to wait {delta_req_time} seconds. Firewall life: {target_reqs - hit_streak}")
    else:  # request accepted
        hit_streak = User.update_wall_counter(username, 1)  # system will raise error before if not accepted
        # User.update_xp(username, 1)
    
    # check if quest is completed and update content accordingly
    # assuming fail / not completed
    state = QuestState.FAILED.value
    User.update_wall_last_req_at(username)  # updating timeout
    content = content_generator.create_content(quest, state, formatting)
    content.update({"status": "trying"})
    content.update({"story": get_success_response(hit_streak, target_reqs) + f" Firewall life: {target_reqs - hit_streak}"})
    if quest_completed(hit_streak, target_reqs):
        state = QuestState.COMPLETED.value
        User.update_quest_state(username, QuestTitle.BEG_QUEST.value, state)
        User.update_xp(username, target_reqs)
    return content


def jason_is_smashing(req: Request) -> bool:
    print("t1")
    json = parser_utils.get_json(req)
    print("t2")
    t, min, max, json_key, json_val = get_quest_vars()
    print("t3")
    print(json)
    print("t4")
    json_says = json.get(json_key, "")
    print("t5")
    if not isinstance(json_says, str):
        raise ValueError('Jasons smashing has to be a bit more... "STRINGent?"')
    print("t6")
    return json_says.lower() == json_val


def get_delta_since_last_req(username: str) -> int:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    last_attempt_at = User.get_wall_last_req_at(username)
    delta_time = (now - last_attempt_at).total_seconds() if last_attempt_at else -1
    return delta_time


def quest_completed(counter: int, target: int) -> bool:
    return counter >= target


def get_success_response(counter, target):
    # Reactions for each successful smash
    SUCCESS_SMASH_REACTIONS = [
        "HEY—stop hitting it like that.",
        "That scorch mark was already there.",
        "Jason looks tired. He won’t last.",
        "Walls are supposed to crack a little.",
        "You call that a smash? I’ve seen worse.",
        "The fire barely noticed. I noticed. Unfortunately.",
        "Don’t establish a rhythm. I hate rhythm.",
        "That was… effective. Don’t do it again.",
        "You’re abusing Jason. I’ll report this.",
        "The wall is fine. It’s fine.",
        "You’re not breaking it—you’re irritating it.",
        "Stop waiting the correct amount of time!",
        "That timing was disgusting.",
        "Jason swung wrong. The wall slipped.",
        "Fire bends sometimes. This means nothing.",
        "You’re just lucky the flames blinked.",
        "I built this wall myself! Badly—but still!",
        "You think repetition scares me?",
        "The wall is barely weaker. Barely.",
        "I can still fix this. I always fix this."
    ]

    # Progressive reactions as wall integrity drops
    PHASE_30_PERCENT = [
        "Okay. That section was cosmetic.",
        "Fire walls shed layers. It’s natural.",
        "You’re clearly overusing Jason.",
        "I expected this part to go faster.",
        "Stop looking confident. It’s rude."
    ]

    PHASE_60_PERCENT = [
        "WHY is the fire making that noise?",
        "You waited exactly right again.",
        "Jason should have burned by now!",
        "I’m adding a rule. I’m THINKING about it.",
        "The wall is regenerating. Any second. Any—"
    ]

    PHASE_LAST_10_PERCENT = [
        "STOP. STOP SMASHING.",
        "I didn’t mean that much endurance!",
        "You’re cheating. Quietly. Somehow.",
        "The wall is just shy. It needs encouragement!",
        "PLEASE WAIT TOO LONG—JUST ONCE."
    ]

    # Final defeat reaction
    FINAL_DEFEAT_REACTION = (
        "NO—NO NO NO NO—\n"
        "THAT WASN’T THE REAL WALL!\n"
        "THAT WAS THE OUTER FIRE!\n\n"
        "...\n\n"
        "I WAS GOING TO FIX IT.\n"
        "I WAS GOING TO ADD MORE FIRE.\n"
        "BIGGER FIRE. BETTER FIRE.\n\n"
        "*sniff*\n\n"
        "You only won because Jason didn’t melt fast enough.\n"
        "This isn’t skill. This is attrition.\n\n"
        "TAKE THE CRUDe CROWN.\n"
        "IT’S TOO HEAVY ANYWAY.\n\n"
        "...\n\n"
        "I DIDN’T EVEN LIKE WALLS."
    )
    
    if counter >= target:
        print("here!")
        return FINAL_DEFEAT_REACTION
    if random.random() < 0.7:
        print("standard")
        return random.choice(SUCCESS_SMASH_REACTIONS)
    if target/counter < 0.33:
        print("30%")
        return random.choice(PHASE_30_PERCENT)
    elif target/counter < 0.66:
        print("60%")
        return random.choice(PHASE_60_PERCENT)
    elif target/counter < 0.90:
        print("90%")
        return random.choice(PHASE_LAST_10_PERCENT)
    return random.choice(SUCCESS_SMASH_REACTIONS)

    
def get_failure_response():
    # Failure responses when timing breaks and the player must restart
    FAILURE_RESET_REACTIONS = [
        "AH! Too slow. The fire stretched and healed. Reset.",
        "You hesitated. The wall enjoyed that. Start over.",
        "That pause was illegal. Jason is now decorative ash.",
        "Ooo, wrong timing. The wall feels brand new!",
        "Reset! I told you the wall regenerates when bored.",
        "You waited too long. The fire licked itself better.",
        "Timing error! Jason crisped like cheap bacon.",
        "That gap was unacceptable. Begin again.",
        "The wall healed. Jason didn’t. Tragic.",
        "Reset complete. Don’t look so surprised."
    ]

    
    JASON_RESPAWN_STORIES = [
    "Oh look! Another Jason just wandered in. Same face. Same name. No memory. Incredible.",
    
    "Jason burned up, but don’t worry—Jason™ units are self-replacing. This one even smells fresher.",
    
    "That Jason is gone. This Jason insists he’s always been here. Don’t argue with him.",
    
    "A new Jason crawls out from behind the wall, stretches, and asks, “Did I miss anything?”",
    
    "Jason melted, but a nearly identical Jason appears holding a coffee and unresolved confidence.",
    
    "That Jason failed. This Jason swears he won’t. They all say that.",
    
    "A replacement Jason drops from above. No one acknowledges it.",
    
    "Jason combusted. Another Jason blinks into existence and cracks his knuckles.",
    
    "You now have Jason (again). He seems eager. Concerningly eager.",
    
    "The fire consumed Jason, but the universe provides. Here’s Jason."
    ]
    
    resp = random.choice(FAILURE_RESET_REACTIONS) + " " + random.choice(JASON_RESPAWN_STORIES)
    return resp
    
    
