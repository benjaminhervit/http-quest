# Http quest
## Project status
The project is current in a poor, most likely broken state, after having been through its first few iteration and a single live test.
Focus is currently on clean up and get a stable framework (no ETA).

## Description
HTTP Quest is a HTTP Client based adventure game framework to teach the basics of using HTTP.
They players will have to send and read HTTP requests to progress in the game.
The player will have to use GET, POST, PUT, DELETE correctly and passing the correct riddle answers as both forms and JSON.
A shared leaderboard website shows how far each player is from completing the game.

The project comes with a predefined path but it is being developed with the intention of easy extensibility and creating custom adventures (see Framework section).

### Player prerequisites
The game requires some basic knowledge of HTTP terminology and a horrible sense of humor and bad puns.
After completing the game, the player should have some basic experience with reading and writing HTTP requests using the browser, a HTTP client and maybe though code if they are up for the challenge. 

### Background
I developed while being an instructor in the course Web of Things at Aarhus University.
In the course, students are being expose to hands-on experience with a wide variety of technologies and tools in a very short time.
As an instructor, my job was to go through exercises with them that would enable them to better make their hand-ins.
This project was an experiment to see how they responded to such exercises and if it should be developed further in the future.

## Framework
### Techstack
The framework is build using Python Flask, SQLite, and vanilla HTML, CSS and JavaScript.
The techstack was chosen based on what the students were learning to keep the code familiar to them (if they shoulld be curious) and to improve my own knowledge and experience for better support.

## Installation
- Python venv and requirements.txt should setup the backend.
- Latest version of vanilla JavaScript should be sufficient.
- Must run on a server (I used PythonAnywhere)
- [ ] More detail to come

### Features
#### Public website 
- Create player (no password or credientials atm).
- Shared public leaderboard
- Game manual

#### Level creator
- Create levels through JSON (hard coded in files)
- Define HTTP settings, e.g. type (GET/POST/PUT/DELETE), body (form/JSON), expected body content.
- Write level introduction, description, riddle, answer, correct response and wrong response.
- Set next level and completion score.

### Folder structure
- [ ] on its way
### Architecture
- [ ] on its way

#### More to come...

## Roadmap
- [ ] Clean up and get current version up and running again.
- [ ] Use database to store levels
- [ ] 
- [ ] Frontend for creating a 
