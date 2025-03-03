from game.level import RegisterLevel, TestLevel, GitLevel, GateLevel, ThroneLevel, CrownLevel
from game.routes import Route as R

def createTheGitLevel():
    level = GitLevel()
    level.set_directions(f'GET to {R.MEET_THE_GIT_MONSTER.value} !!!')
    level.set_description("As you arrive, a familiar stench catches your nose. It is the smell of rotten branches. You are not in doubt: A git monster is approaching and you must find a way to paralyze it.")
    level.set_hint('Let me goggle that for you... nooooooot')
    level.set_quest(f'If you can remember the right order of the paralysis spell, the you can PUT {R.STUN_THE_GIT_MONSTER.value} the git monster to sleep - at least for a while. How was it? pull commit add push? or... push commit pull add? or was it force rebase merge origin? If you do it right, you have a 20% URL chance to succeed')
    level.set_wrong_answer_response("Your words are poorly chosen and you and your party is drowning in error messages and merge conflicts Hurry! Try again before it is too late!")
    level.set_victory_message_template("The git monster falls into a deep paralysis as you yell git add . git commit -m 'work for fucks sake!' - but you suspect it is only for a while, so you hurry on before it wakes up again.")
    return level

def createRegisterLevel():
    the_register_level = RegisterLevel()
    the_register_level.set_directions('It all begins at the beginning...')
    the_register_level.set_description('Welcome to Ready Player WoT.')
    the_register_level.set_quest('You must register your party to take on this CRUDe quest.')
    the_register_level.set_directions('I am pretty sure there is a registration site somewhere in the TAs sandbox.')
    the_register_level.set_hint('I am pretty sure there is a registration site somewhere in the TAs sandbox.')
    the_register_level.set_victory_message_template("Thank you for taking on this CRUDe quest! Wauw... {party} is such as cool name... ... Anyway! This is JaSON. You should take him with you as your translator. Also, consider bring a POSTMAN along as well. They can be very APPlicable in more situations than one might think. Best of luck!")
    return the_register_level

def createTheTestLevel():
    the_test_level = TestLevel()
    the_test_level.set_directions(f'GET to {R.THE_TEST_BEGINS.value} and do not forget your towel!')
    the_test_level.set_description("You stand in front of an old wise sage who, without considering if you are actually listening, begins to speak: ")
    the_test_level.set_quest('To know that you are worthy, you must answer: Answer to the Ultimate Question of Life, The Universe, and Everything?')
    the_test_level.set_hint(f"Grab your towel and hitch a hike around the internet and you will find what you are seeking. When you have an answer, POST it to {R.THE_TEST_ANSWER.value}.")
    the_test_level.set_wrong_answer_response('Something is not right.')
    the_test_level.set_victory_message_template("That is correct, {party}! You are truly enlightened! Alas, if only we knew had known what the Ultimate Question of Life, the Universe, and Everything is - but there is not time! Something is approaching that only you can fix!")
    return the_test_level

def createGateLevel():
    level = GateLevel()
    level.set_directions(f'GET to {R.THE_GATE.value} while you can!')
    level.set_description('Your path is blocked by a giant gate (who would have seen that coming?).')
    level.set_hint('I hope you have been nice to JaSON. If you tell him {\party:here , answer:here}\, he can translate on your behalf')
    level.set_quest(f'To open {R.THE_GATE_OPEN.value} you must DELETE it - but you have not taken your pre-workout shake today. Instead, you must [answer] an riddle in old forgotten language: "Speak friend and enter..."')
    level.set_wrong_answer_response("Someone has not been practising speaking elvish for a while. Try again.")
    level.set_victory_message_template('As the gate vanishes, you hear the git monster awakening. Better get away fast!')
    return level

def createThroneLevel():
    level = ThroneLevel()
    level.set_directions(f'To GET inside {R.THE_THRONE.value} JaSON must speak you party:name and nothing else.')
    level.set_description('You find yourself in a big hall with a majestic-ish throne at the other end: The WoThrone™. As you get closer, the council to the throne appear from the shadows and walk in respectful distance behind you. HTML, CSS, SQL, JavaScript, Python... is that venv with a... bottle? ... you... no. way... GIT!? ... Anyway! they wish no your harm.')
    level.set_quest('Standing in fron of the throne you see the CRUDe Crown and you know that you are worthy to PUT it on. But how?')
    level.set_hint(f'JaSON seems to know the answer but can you ask him the right question to PUT on {R.THE_CROWN.value}?? Maybe if try to {R.SPEAK_TO_JASON.value} in his own language, POSTing your party name and keep thinking about why_the_crown_is_cool in your HEAD - then maybe he will tell you?')
    level.set_wrong_answer_response("JaSON smiles but remains silent. This is not it. Have you remembered to use you head?")
    level.set_victory_message_template('HOLY FUCK! JaSON exlaims when he realises that you are now using telepathy-ish to communicate with him. I will tell you anything but just use your body like a normal person next time! body: talk. head: you. okay? Holy...')
    return level

def createCrownLevel():
    level = CrownLevel()
    last_instructions = f'JUST... Request with method PUT to {R.THE_CROWN.value} and body as JSON: {{"answer":"i have a cool new hat", "motiviation":"why you want the crown (this will be publicly available on day by the way)"}} and in your HEADER {{"party":"party_name"}}. How hard can it be?! And my name is not JaSoOoNn but Terry! I do not know why people keep calling me that...'
    level.set_directions(last_instructions)
    level.set_quest('In case JaSONs immature outburst made you forget the setting: Throne. Council. Put on the Crown.')
    level.set_hint(last_instructions)
    level.set_wrong_answer_response("JaSON look at you with a thousand yeard stare, a frozen smile and what seems like a twitching eye... I think we broke JaSON? Lets try again...")
    level.set_victory_message_template('You PUT on the CRUDe CROWN victoriously and high fives all of the council while ignoreing JaSONs sulky attitude. You did it! You are now the Ruler of WoT with a cool hat. Well done!')
    return level