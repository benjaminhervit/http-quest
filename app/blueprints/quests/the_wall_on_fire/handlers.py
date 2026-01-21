from flask import Request
from datetime import datetime, timezone
import random

from app.quest import QuestData
from app.utils import content_generator, parser_utils
from app.enums import QuestState, QuestTitle
from app.models import User
from app.authentication_manager import authenticator
from app.errors import QuestError, GameError


def get_quest_vars():
    return (3, 3, 10, "jason", "smash!", "twinkle twinkle little star, now you are going to a farm")  # total, min, max, json_key, json_val, final song


def get_handlers():
    return {"GET": get_handler, "PUT": put_handler, "DELETE": delete_handler}


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


def put_handler(quest: QuestData, req: Request):
    print("1")
    # setup
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.WALL_QUEST.value)
    
    # quest vars
    target_reqs, min_wait, max_wait, json_key, json_val, lyrics = get_quest_vars()
    formatting = {"HERO": username,
                  "TOTAL_REQS": target_reqs,
                  "MIN_WAIT": min_wait,
                  "MAX_WAIT": max_wait,
                  "JSON_KEY": json_key,
                  "JSON_VAL": json_val
                  #"LYRICS": lyrics,
                  }
    # quest is locked
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    
    print("2")
    # quest is completed
    wall_is_destroyed = User.get_wall_destroyed(username)
    if wall_is_destroyed and state == QuestState.COMPLETED.value:
        content = content_generator.create_content(quest, state, formatting)
        content.update({"story": "Stop itZzz.. It's already brokenZZzzZZzz... You.... are litZzzz...terally... justZZZzZZzzbeating... a pile of broken... brickZZZZZZZZzzzz... What... is. wrong.... with.... ZzzzzzzzZZZzzzz. It seems like the wall and the horific little create are connected even when it is asleep"})
        content.update({"quest": get_sleep_quest(lyrics)})
        content.update({"learning": get_final_learning()})
        return content
    # player has not destroyed the wall yet
    if wall_is_destroyed is False:
        content = content_generator.create_locked_content(quest)
        content.update({"story": "First, focus on DELETE-ing the wall, then you will learn what to do here."})
        return content
    # player has to put the creature to sleep
    json = parser_utils.get_json(req)
    lullaby: str = json.get("sing", "")
    if not lullaby:
        raise QuestError(f"He may not be Papparoti or Taylor Switft but Jason really need to sing:'{lyrics}' to PUT this creator to sleep.")
    if lullaby.lower() != lyrics:
        raise QuestError(f"Great! Jason is singing BUT whatever this song is: '{lullaby}' - it isn't '{lyrics}'")
    
    # player should have succeeded
    state = QuestState.COMPLETED.value
    User.update_quest_state(username, QuestTitle.WALL_QUEST.value, state)
    User.update_xp(username, quest.xp)
    
    content = content_generator.create_content(quest, state, formatting)
    content.update({"story": ("You immediately regret asking Jaons to sing." 
                              "twInKle TWiNKLE little STAR... Jasons voice sounds like a thousand cats being forced bathed by an elderly well-meaning-but-less-perceptive elderly lady."
                              "But apparently the creature has no idea what singing is supposed to sound like. Its eyes turns big in awe and within 10, horrible, painful singing seconds, it falls into a deep sleep, cuddling with the nearest brick from the wall."
                              "Finally, you can ask Jason to stop torturing his surroundings (unfortunately, he seems to have taken a liking this 'singing'). "
                              "There are no more challenges ahead and you can now claim the CRUDe Crown!"
        )})
    content.update({"learning": get_final_learning()})
    return content


def get_final_learning() -> str:
    return "Well done! This was the big 'test' in the game. You have used both GET, DELETE and PUT and managed to maked timed, valid JSON requests with authorization."


def delete_handler(quest: QuestData, req: Request):
    # setup
    username = authenticator.authenticate_with_username(req)
    state = User.get_user_quest_State(username,
                                      QuestTitle.WALL_QUEST.value)
    
    # quest vars
    hit_streak = User.get_wall_counter(username)
    target_reqs, min_wait, max_wait, json_key, json_val, lyrics = get_quest_vars()
    formatting = {"HERO": username,
                  "TOTAL_REQS": target_reqs,
                  "MIN_WAIT": min_wait,
                  "MAX_WAIT": max_wait,
                  "JSON_KEY": json_key,
                  "JSON_VAL": json_val
                  }
    
    if state == QuestState.LOCKED.value:
        return content_generator.create_locked_content(quest)
    
    wall_is_destroyed = User.get_wall_destroyed(username)
    if wall_is_destroyed and state == QuestState.COMPLETED.value:
        content = content_generator.create_completed_content(quest)
        content.update({"story": "Stop itZzz.. It's already brokenZZzzZZzz... You.... are litZzzz...terally... justZZZzZZzzbeating... a pile of broken... brickZZZZZZZZzzzz... What... is. wrong.... with.... ZzzzzzzzZZZzzzz. It seems like the wall and the horific little create are connected even when it is asleep"})
        return content
    
    if wall_is_destroyed:
        content = content_generator.create_completed_content(quest)
        content.update({"story": get_wall_destroyed_reaction()})
        content.update({"quest": get_sleep_quest(lyrics)})
        return content
    
    # validate that the json input
    if jason_is_smashing(req) is False:
        raise QuestError("... You need to get Jason to smash!")
    
    # validate the request timing
    delta_req_time = get_delta_since_last_req(username)
    if delta_req_time < 0:
        raise GameError("Something went wrong with the request delta time and it is not on you. Talk with a TA.")
    
    if delta_req_time < min_wait or delta_req_time > max_wait:  # check if requesting too fast
        hit_streak = User.set_wall_counter(username, 0)
        User.update_wall_last_req_at(username)
        resp = get_failure_response()
        raise QuestError(f"{resp}. You decided to wait {delta_req_time} seconds. Firewall life: {target_reqs - hit_streak}")
    else:  # request accepted
        hit_streak = User.update_wall_counter(username, 1)  # system will raise error before if not accepted
        if hit_streak > target_reqs:
            User.set_wall_counter(username, target_reqs)
    
    # check if quest is completed and update content accordingly
    # assume fail and then check for success
    User.update_wall_last_req_at(username)  # updating timeout
    content = content_generator.create_content(quest, state, formatting)
    content.update({"status": "trying"})
    content.update({"story": get_success_response(hit_streak, target_reqs) + f" Firewall life: {target_reqs - hit_streak}"})
    if final_hit(hit_streak, target_reqs):
        User.update_xp(username, target_reqs)
        User.set_wall_destroyed(username, True)
        content = content_generator.create_content(quest, state, formatting)
        content.update({"story": get_wall_destroyed_reaction() + f" Firewall life: {target_reqs - hit_streak}"})
        content.update({"quest": get_sleep_quest(lyrics)})
    return content


def jason_is_smashing(req: Request) -> bool:
    json = parser_utils.get_json(req)
    _, _, _, json_key, json_val, _ = get_quest_vars()
    json_says = json.get(json_key, "")
    if not isinstance(json_says, str):
        raise ValueError('Jasons smashing has to be a bit more... "STRINGent?"')
    return json_says.lower() == json_val


def get_delta_since_last_req(username: str) -> int:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    last_attempt_at = User.get_wall_last_req_at(username)
    delta_time = (now - last_attempt_at).total_seconds() if last_attempt_at else -1
    return delta_time


def final_hit(counter: int, target: int) -> bool:
    return counter >= target


def get_wall_destroyed_reaction() -> str:
    response = (
        "NO—NO NO NO NO—\n"
        "You were not supposed to do that! " 
        "Look at my wall! My mighty wall! We still had so much to experience together! "
        "So many HerOES to annoy! .... hehehehehe..... Luckily I can just build a new one\n"
        "THAT WASN’T THE REAL WALL!\n"
        "THAT WAS THE OUTER FIRE!\n\n"
        "I AM GOING TO ADD MORE FIRE!\n"
        "BIGGER FIRE! BETTER FIRE! MWHAHEHEHEHIHIHAHAHA\n\n")
    return response


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
    
    if random.random() < 0.6:
        return random.choice(SUCCESS_SMASH_REACTIONS)
    if target/counter < 0.33:
        return random.choice(PHASE_30_PERCENT)
    elif target/counter < 0.66:
        return random.choice(PHASE_60_PERCENT)
    elif target/counter < 0.90:
        return random.choice(PHASE_LAST_10_PERCENT)
    return random.choice(SUCCESS_SMASH_REACTIONS)


def get_sleep_quest(lyrics) -> str:
    return f"You cannot let this foul creature continue its reign of annoyance. URL have to PUT it to sleep once and for all. You know, just like the wet did with your dog when you were a kid. PUT Jason to sing:'{lyrics}'"
 
    
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