# Chatroom

## What is this project?
This is a portfolio project.
It's a chatroom platform that users can join different chatrooms and send messages to each other, with auto update and auto scroll for messages.

## Highlights and features

**Frontend - Backend - Database**
This is my first project working with database and second project with a Python backend.

**A mix of learned and new skills**
- Javascript for frontend, styled with CSS
- Python for backend and request handling, with Aiohttp to assist with web functions(??????)
- MongoDB for database
- Docker to containerise the backend and database
- SourceTree for version control
- GitBash for Git command for connecting local and remote repo
(should this one be a separate item?????? i first had it grouped with source tree)
- GitHub to host remote repo for easy access, with a README.md

**Chatroom functionalities**
- create user name
- on top of the default chatroom, users can create new chatroom
- with a list of chatrooms, easy switch between different chatrooms
- showing existing messages from activated chatroom(max 100) when first entered
- auto scroll to show latest messages
- auto-update message per second after entering a chatroom

##  How to run the porject
What you need? [GitBash/Terminal](?????) and Docker

To run the frontend
```
$ cd /chatroom/front
$ quasar dev
```

To run the backend and database(required to be on the same network)
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
- work with official library for Python
- running a Docker contain of Mongo databse with the backend

2. Using user-defined Docker network
Running 2 containers run on a user defined network simultaneously is a new [thing to do???].
(this bit of text probably doesn't match with the title at the moment. but i don't know how to phrase it -,-)

3. Better understanding for request handling and asynchronous functions
To handle request and work the database methods for insert/retrieve data, needs a good understanding of coroutine and how to properly implement it.
In this specific project, to run the backend async was not neccessary, but it was good to have it implemented(?????)

4. Aiohttp
(i don't know what to write here TTATT bb heeeeeeeelp)

5. SourceTree authentication problem
There was a bug in SourceTree affecting its ability to authenticate and connect to GitHub.
Though authentication seemed successful, connection from SourceTree desktop app to remote repo was failed.
SourceTree has a nice UI for version control, so I continued to use it for that purpose.
However, I had to use Git commands for anything related to the remote repo.

## What did I do well
1. It works!
2. Upgraded endpoint calling to query successfully(????)
3. Worked with async Python driver for Mongo(may not be neccessary due to project scale)
6. Concise and logical commit and commit messages(for this one can you look at my commit msgs please TAT)
5. Configed ESLint rules to fit personal preference and prevent minor lint issues stop compilation.(?????????)
4. Implemented auto scroll for message display, with mechanics to pause/resume it. Bonus "jump to bottom" button
3. Improved CSS skill, such as:
- style by html tags
- responsive element size
- element alignment
- explored new CSS settings such as overflow-wrap, border-radius, and box-sizing

## What did I do not so well
1. Mixed up projects in one folder
There was an attempt to make a template based on this specific folder.
At one point it was mixed with this project but removed later.

2. Messed up init commit
Authentication and connection problem with SourceTree grately discouraged me to use the software at the beginning of the project.
Init commit was made half way development. It was not ideal in both version histroy/control and ???? wise(??????).

## Goal for coming prjects
1. Start new project for separate tasks, alternatively, branch out if it's a feature related to the main project
2. Try fixing SourceTree

### Verions of software for reference        
Frontend: vue 3.0, quasar 2.0;
Backend: Python 3, Docker
Database: MongoDB official docker image[latest][^1]

[^1]: This project was running latest version of official Mongo image at the beginning of development.
  It was updated midway development. The closest version to the initial version would be 5.0.9
  This is for future refrence in case future versions of Mongo are not compatible.(??????????)

This is the template for new porjects with JS fronted and Python backend

Frontend: vue 3.0, quasar 2.0, npm 8.5.5, nodejs 16.14.2; 
Backend: python 3, docker only

ver 1.0
fixed eslint rules: 4 space indent; no space before function parenthesis; semi colon at the end; double quotes for strings