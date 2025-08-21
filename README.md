# ReQUEST
! OBS ! Please go to the KISS branch for the most stable version

ReQUEST is a HTTP Client based adventure game to teach the basics of HTTP and CRUD to students that are new to programming.
To play the game, the player will send and read HTTP requests, using the browser, a client (e.g. Postman), or writing their own scripts.
The player will have to use basic methos (GET, POST, PUT, DELETE) together with the right data format (Query, JSON, Form, path, headers) to complete quests.
A shared leaderboard website shows how far each player is from completing the game.

## Project status
For self-educational purposes, I am currently rewriting the project as an extendable and scalabe framework, using TDD methodologies.
Therefore, only the two first quests are currently working: Welcome, and Accept Quest.

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
The techstack was originally chosen based on the students coriculum but SQLite was replaced with SQL Alchemy for the framework because the models layout appealed to me. 

## Installation (local testing and try out)
The current version
- Install and activate .venv with requirements.txt
- Run pytest in terminal to validate that everything (tested) works.
- Run flask run --debug in terminal and the leaderboard should open

### Features
#### Public website 
- Create player (no password or credientials atm).
- Shared public leaderboard
- Game manual

### Architecture
![ReQUEST framework](https://github.com/user-attachments/assets/3fdd755c-1005-4369-98d6-9ed9625a1160)

## System overview diagram
The diagram below models the complete lifecycle of a player request in reQUEST.
It the players entry and interaction loop together with the technical flow the HTTP request through parsing, validtiong, authorizing, and executing game logic, including expected error messages that is returned to the player. 

![reQUEST_system_overview](https://github.com/user-attachments/assets/146c1a3a-abc4-4b25-bd14-d4d5707ee810)

Key system features include:
- Modular route and request handling via Flask blueprints
- Stateless vs stateful quest support
- Player:Quest state management (locked, completed, failed)
- Error handling via standard HTTP codes (400, 401, 404, 500)
- JSON-based output

## Roadmap
### MVP aka. v1.0: All Quests
- [ ] Add all identified tests
- [ ] Add Quest 3: Signup for the quest! support and tests for POST and Form.
- [ ] Add quest 4: Learn telekinese: support and tests for identifier in headers
- [ ] Add quest 5: Get your squire Jason! Support and tests for JSON
- [ ] Add quest 6: Get some armor on! Support and tests for PUT
- [ ] Add quest 7: Slay the Git monster! Support and tests for DELETE

### v1.1: Quest renderer
- [ ] All quests can be returned as JSON or HTML based on param in query.

### v1.2: Story branching
- [ ] Quests can have multiple precessors.
- [ ] Precessors can be optional for unlocking a quest.
- [ ] No armor - no git slaying! : Quest 7 is available without quest 6 - but requires armor to complete

### v1.2: Create custom quests
- [ ] Players can create their own quests with HTTP requests.

## Credits
Thank you to Abdelhadi Dyouri and Caitlin Postal for this tutorial: https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy#step-5-adding-flask-sqlalchemy-models-to-your-flask-application
