from fastapi import FastAPI

import uuid
import random
from enum import Enum

app = FastAPI()
games = {}
usergames = {}
userscores = {}

@app.get("/")
async def root():
    return {"message":"Set a user"}

@app.get("/newgame/{user}")
async def root(user):
    uid = str(uuid.uuid4())
    if usergames[user] is not None:
        del games[usergames[user]]
        userscores[user] = userscores[user] - 1
    games[uid] = newGameStart(user)
    usergames[user] = uid
    return {"game":uid}

@app.get("/games")
async def root():
    return list(games.keys())

@app.get("/userscores")
async def root():
    return userscores

@app.get("/guess/{game}/{a}/{b}/{c}/{d}")
async def guess(game,a,b,c,d):
    games[game]["move"] += 1
    results = check([a,b,c,d],games[game]['answer'])
    if results[1] == 4:
        del games[game]
        userscores[game["user"]] = userscores[game["user"]] + 1
    return {"num_right_place":results[1],"num_right_colour":results[0],"guess":games[game]["move"]}

def check(guess, answer):
    return sum(min(sum(1 for i in [guess[i] for i in [i for i in range(len(answer)) if guess[i] != answer[i]]] if i == c), sum(1 for i in [answer[i] for i in [i for i in range(len(answer)) if guess[i] != answer[i]]] if i == c)) for c in set(answer)), len(answer) - len([i for i in range(len(answer)) if guess[i] != answer[i]])

def newGameStart(user):
    return {
        "move":0,
        "answer":[
                str(random.choice(list(Colours)).name),
                str(random.choice(list(Colours)).name),
                str(random.choice(list(Colours)).name),
                str(random.choice(list(Colours)).name)
            ],
        "user":user
    }
    

class Colours(Enum):
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5