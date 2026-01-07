
<img width="888" height="737" alt="Screenshot 2025-09-07 at 21 52 43" src="https://github.com/user-attachments/assets/447b3c72-6fcc-42a4-9574-4f69bf50a873" />

# ReQUEST
ReQUEST is a HTTP Client based educational adventure game to teach the basics of HTTP and CRUD to students in the course Web of Things on Aarhus University. It is a hobby project that I build as a Teaching Assistant and only a supplement of fun to the actual coriculum. To play the game, the player will send and read HTTP requests, using the browser, a client (e.g. Postman), or writing their own scripts.
The player will have to use basic methos (GET, POST, PUT, DELETE) together with the right data format (Query, JSON, Form, path, headers) to complete quests.
A shared leaderboard website shows how far each player is from completing the game.

## Project status
For self-educational purposes, I am currently rewriting the project as an extendable and scalabe framework, using TDD methodologies.
Therefore, only the two first quests are currently working: Welcome, and Accept Quest.

## Credits
Thank you to Abdelhadi Dyouri and Caitlin Postal for this tutorial: https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy#step-5-adding-flask-sqlalchemy-models-to-your-flask-application


## Quik-start
- Download the repo
- Create a python .venv and activate it
- Install the requirements.txt
- From project root in the terminal: `python run.app` or `flask run`
This should give you a clean local version to play around with.

### Player prerequisites
The game requires some basic knowledge of HTTP terminology and a horrible sense of humor and likability of bad puns.
After completing the game, the player should have some basic experience with reading and writing HTTP requests and some of the standards.

### Background
I developed the game while being an instructor in the course Web of Things at Aarhus University.
In the course, students learn to use a wide variety of technologies and tools in a very short time: python, JS, HTML, CSS, SQL.
As an instructor, my job was to go through exercises and help them with their hand-ins.
This project was an experiment to see how they responded to such exercises and if it should be developed further in the future.

## Framework
### Techstack
The framework is build using Python Flask, SQL Alchemy, and vanilla HTML, CSS and JavaScript.
The techstack was originally chosen based on the students coriculum but SQLite was replaced with SQL Alchemy for better scaling later on.

### Features
#### Public website 
- Create player (no password or credientials atm).
- Shared public leaderboard
- Game manual

## Roadmap
### MVP aka. v1.0: All Quests
- [x] Quest 1: learn about path extension in browser.
- [x] Quest 2: learn about form and post.
- [x] Quest 3: learn about authorization header.
- [x] Quest 4: learn about json and post.
- [ ] Quest 5: learn about accessing request logs (game specific)
- [ ] Quest 6: learn about PUT.
- [ ] Quest 7: learn about DELETE.

### v1.1: Quest renderer
- [x] All quests can be returned as JSON or HTML based on param in query.
- [ ] Quests have precessors that needs to be unlocked.

### v1.2: Story branching
- [ ] Quests can have multiple precessors.
- [ ] Precessors can be optional for unlocking a quest.
- [ ] No armor - no git slaying! : Quest 7 is available without quest 6 - but requires armor to complete

### v1.2: Create custom quests
- [ ] Players can create their own quests with HTTP requests.

## Known issues
- [ ] Leaderboard is currently broken due to refactor of the data schema. 
- [ ] Identification quest needs to be updated to the new quest handling format
- [ ] Jaon quest needs to be updated to the new quest handling format
- [ ] The wall quest needs to be updated to the new quest handling format
- [ ] The monster quest needs to be updated to the new quest handling format
- [ ] The crown quest needs to be updated to the new quest handling format