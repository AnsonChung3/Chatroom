# Chatroom

This is a portfolio project.

It's a chatroom platform that users can join different chatrooms and send messages to each other, with auto update and auto scroll for messages.

## Highlights and features

**Frontend - Backend - Database**
This is my first project working with database and second project with a Python backend.

**A mix of learned and new skills**
- Javascript for frontend, styled with CSS
- Python for backend and request handling, with Aiohttp
- MongoDB for database
- Docker to containerise the backend and database
- SourceTree for version control
- GitHub to host remote repo for easy access, with a README.md

**Chatroom functionalities**
- create user name
- on top of the default chatroom, users can create new chatroom
- with a list of chatrooms, easy switch between different chatrooms
- showing existing messages from activated chatroom(max 100) when first entered
- auto scroll to show latest messages
- auto-update message per second after entering a chatroom

##  How to run the porject
To run the frontend
```
cd /chatroom/front
npm install
quasar dev
```

To run the backend and database(required to be on the same network), presuming the frontend is running on 8080
```
$ cd /chatroom/back
$ docker build -t chatroom_backend .
$ docker network create portfolio_network
$ docker run --name mongodb --network portfolio_network -d -e MONGO_INITDB_ROOT_USERNAME=username -e MONGO_INITDB_ROOT_PASSWORD=password mongo:5.0.9
$ docker run --name chatroom_backend_container --network portfolio_network -d -p 8181:8080 -e MONGODB_CONNSTRING=mongodb://username:password@mongodb chatroom_backend
```

## Challenges when developing
1. Using MongoDB
This is the first time for me to use any databse. I acquired some new skills along development:
- understand how databse work
- navigate through documentations for database methods
- work with Motor, the official driver for Python
- running a Docker contain of Mongo databse with the backend

2. Using user-defined Docker network
Running 2 containers run on a user defined network simultaneously.

3. Better understanding for request handling and asynchronous functions
To handle request and work the database methods for insert/retrieve data, needs a good understanding of coroutine and how to implement it.
In this specific project, to run the backend async was not neccessary, but it was nice to have.

4. SourceTree authentication problem
There seemed to be a bug in SourceTree affecting its ability to authenticate and connect to GitHub.
Though authentication seemed successful, connection from SourceTree desktop app to remote repo failed.
SourceTree has a nice UI for version control, so I continued to use it to commit.
However, I had to use Git commands to push.

## What did I do well
1. It works!
2. Upgraded endpoint calling to query
3. Worked with async Python driver for Mongo(may not be neccessary due to project scale)
6. Concise and logical commit messages
5. Configed ESLint rules to prevent minor issues stop compilation
4. Implemented auto scroll for message display, with mechanics to pause/resume it, with a bonus "jump to bottom" button
3. Improved CSS skill, such as:
- style by html tags
- responsive element size
- element alignment
- explored new CSS settings such as overflow-wrap, border-radius, and box-sizing

## What did I do not so well
1. Mixed up projects in one folder
There was an attempt to make a template based on this specific folder.
Template related content was removed in the process of doing this project.

2. Messed up init commit
Authentication and connection problem with SourceTree grately discouraged me to use the software at the beginning of the project.
Init commit was made half way development. It was not ideal in both version histroy/control.

## Goal for coming prjects
1. Start new project for separate tasks, alternatively, branch out if it's a feature related to the main project
2. Try fixing SourceTree

### Verions of software for reference        
Frontend: vue 3.0, quasar 2.0;
Backend: Python 3, Docker
Database: MongoDB official docker image[latest][^1]

[^1]: This project was running latest version of official Mongo image at the beginning of development.
  The closest version to the initial version would be 5.0.9 which is included in the How to Run section above.
