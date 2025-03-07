from game.level import RegisterLevel, TestLevel, GitLevel, GateLevel, ThroneLevel, CrownLevel, JasonLevel, GameOverLevel
from game.routes import Route as R

def createRegisterLevel():
    the_register_level = RegisterLevel()
    the_register_level.set_directions('It all begins at the beginning...')
    the_register_level.set_description('Welcome to Ready Player WoT.')
    the_register_level.set_quest('You must register your party to take on this CRUDe quest.')
    the_register_level.set_directions('I am pretty sure there is a registration site somewhere in the TAs sandbox.')
    the_register_level.set_hint('I am pretty sure there is a registration site somewhere in the TAs sandbox.')
    the_register_level.set_victory_message_template("Thank you for taking on this CRUDe quest! Wauw... {party} is such as cool name... ... Anyway! This is JaSON. He is great a translating and giving information. Might as well become good friends from the beginning. Also, consider bring a POSTMAN along as well. They can be very APPlicable in more situations than one might think. Best of luck!")
    return the_register_level

def createTheTestLevel():
    the_test_level = TestLevel()
    the_test_level.set_directions(f'GET to {R.THE_TEST_BEGINS.value} and do not forget your towel!')
    the_test_level.set_description("You stand in front of an old wise sage who, without considering if you are actually listening, begins to speak: ")
    the_test_level.set_quest(f'To know that you are worthy, you must answer: Answer to the Ultimate Question of Life, The Universe, and Everything? When you have an answer, POST it to {R.THE_TEST_ANSWER.value}.')
    the_test_level.set_hint(f"Grab your towel and hitch a hike around the internet and you will find what you are seeking.")
    the_test_level.set_wrong_answer_response('Something is not right.')
    the_test_level.set_victory_message_template("That is correct, {party}! You are truly enlightened! Alas, if only we knew had known what the Ultimate Question of Life, the Universe, and Everything is - but there is not time! Something is approaching that only you can fix!")
    return the_test_level

def createTheGitLevel():
    level = GitLevel()
    level.set_directions(f'GET to {R.MEET_THE_GIT_MONSTER.value} !!!')
    level.set_description("As you arrive, a familiar stench catches your nose. It is the smell of rotten branches. There is no doubt: A git monster is approaching and you must find a way to paralyze it.")
    level.set_hint('Those who has suffered the most will know. Pull-up Addiction comes from Commitment and Pushing through.')
    level.set_quest(f'If you can remember the right order of the paralysis spell, the you can PUT {R.STUN_THE_GIT_MONSTER.value} the git monster to sleep - at least for a while. How was it? pull commit add push? or... push commit pull add? or was it force rebase merge origin?')
    level.set_wrong_answer_response("Your words are poorly chosen and you and your party is drowning in error messages and merge conflicts Hurry! Try again before it is too late!")
    level.set_victory_message_template("As you yell \" git add . git commit -m 'work for fucks sake!' git pull git push \", the git monster is stunned by surprise. No one gets that right! But you suspect it will not last long before it get to its senses again, so you hurry on before it wakes up again.")
    return level

def createGateLevel():
    level = GateLevel()
    level.set_directions(f'GET to {R.THE_GATE.value} while you can!')
    level.set_description('Your path is blocked by a giant gate (who would have seen that coming?).')
    level.set_hint(f'I hope you have been nice to JaSON because this is his home turf. If you tell him {{party_name:<here> , answer:<there>}}, he can speak on your behalf')
    level.set_quest(f'To open {R.THE_GATE_OPEN.value} you must DELETE it - but you have not taken your pre-workout shake today. Instead, you must {{answer}} an riddle in an old forgotten language: \"Speak friend and enter...\"')
    level.set_wrong_answer_response("Someone has not been practising speaking elvish for a while. Try again.")
    level.set_victory_message_template('As the gate vanishes, you hear the git monster awakening. Better get away fast!')
    return level

def createThroneLevel():
    level = ThroneLevel()
    level.set_directions(f'To GET inside {R.THE_THRONE.value} JaSON must speak your {{party_name:here}} and nothing else.')
    level.set_description('You find yourself in a big hall with a majestic-ish throne at the other end: The WoThrone™. As you get closer, the council to the throne appear from the shadows and walk in respectful distance behind you. HTML, CSS, SQL, JavaScript, Python... is that venv with a... bottle? ... you... no. way... GIT!? ... Anyway! they wish no your harm. Now standing in front of the throne, you notice something is missing. WHERE IS THE CRUDe CROWN?! It cannot be far but something tells you that there is (at least) one last trick you need to pull out your HEAD.')
    level.set_quest(f'To GET {R.THE_CROWN.value} you must first {R.READ_JASONS_MIND.value} with your just discovered-out-of-lazy-writing telepathic super powers. It is a delicate task: you must speak with your body {{\"party_name\": <party_name>, \"speak":\"jason\"}} to JaSON and at the same time you must {{\"Authorization\":\"where is the crown\"}} in your HEAD...er. You do it right, you will find the answer in his HEAD...er.')
    level.set_hint(f'Look inside the HEAD...er of JaSONs response. All that you need should be there')
    level.set_wrong_answer_response("JaSON smiles but remains silent. This is not it. Have you remembered to use you head?")
    level.set_victory_message_template('\"HOLY FUCK WHO IS DOING THAT?!\" JaSON exlaims when he realises that someone is using telecenetic powers on him.')
    return level

def createSpeakToJasonLevel():
    level = JasonLevel()
    level.set_directions(f'To GET inside {R.THE_THRONE.value} JaSON must speak your {{party_name:here}} and nothing else.')
    level.set_description(f"You did it! The last piece of the puzzle is hiding in his HEAD...er!")
    level.set_quest(f'To GET {R.THE_CROWN.value} you must {R.READ_JASONS_MIND.value} with your just discovered-out-of-lazy-writing telepathic super powers. Look inside the HEAD...When you speak Jasons name while thinking where is the crown.')
    level.set_hint('In your HEAD think: \"where is the crown\" while you emBODY speak: \"jason\"\ together with your party_name. If you do it right (if PythonAnywhere is not blocking custom headers), you will find the answer in Jasons HEAD...er.')
    level.set_wrong_answer_response("JaSON smiles and looks at you friendly. It is not working. Have you remembered to use you head?")
    level.set_victory_message_template('\"HOLY FUCK WHO IS DOING THAT?!\" JaSON exlaims when he realises that someone is using telecenetic powers on him.')
    return level

def createCrownLevel():
    level = CrownLevel()
    level.set_description = "You are at the end. All that is left is to claim the CRUDe Crown."
    last_instructions = f'Request with method PUT to {R.THE_CROWN.value} and body as JSON: {{\"answer\":\"give me my new cool hat jason\",  \"party_name\":<party_name>, \"feedback\":<OPTIONAL feedback about the game and if you have learne anything.}}.'
    level.set_directions(last_instructions)
    level.set_quest('In case JaSONs immature behaviour made you forget what is going on: Throne. Council. Put on the Crown.')
    level.set_hint(last_instructions)
    level.set_wrong_answer_response("JaSON look at you with a thousand yeard stare, a frozen smile and what seems like a twitching eye... I think we broke JaSON? Is there such a thing as too much telepathy? ... Lets try again...")
    level.set_victory_message_template('CONGRATULATIONS! With a swift movement you take the CRUDe Crown from JaSON and PUT it victoriously on your head as the rest of the council breaks into cheers. As you are doing your victory round, high fiving everyone from the council, JaSON decides that he needs a vacation. You did it! You are now the Ruler of CRUD with a cool hat. Well done! Thank you for playing.')
    return level

def createGameOverLevel():
    level = GameOverLevel()
    level.set_direction = "That's it! You did it! Done!"
    return level