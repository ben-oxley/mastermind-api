from fastapi import FastAPI

import uuid
import random
from enum import Enum

app = FastAPI()
games = {}

@app.get("/")
async def root():
    return {"message":"Set a user"}

@app.get("/newgame")
async def root():
    uid = str(uuid.uuid4())
    games[uid] = newGameStart()
    return {"game":uid}

@app.get("/games")
async def root():
    return list(games.keys())

@app.get("/guess/{game}/{a}/{b}/{c}/{d}")
async def guess(game,a,b,c,d):
    num_right_place = 0
    num_right_place += games[game]['answer'][0]==a
    num_right_place += games[game]['answer'][1]==b
    num_right_place += games[game]['answer'][2]==c
    num_right_place += games[game]['answer'][3]==d
    arr = count(None, a)
    arr = count(arr, b)
    arr = count(arr, c)
    arr = count(arr, d)
    answerarr = count(None, games[game]['answer'][0])
    answerarr = count(answerarr, games[game]['answer'][1])
    answerarr = count(answerarr, games[game]['answer'][2])
    answerarr = count(answerarr, games[game]['answer'][3])
    num_right_colour = 0
    for i in list(Colours):
        if answerarr[str(i.name)] >= arr[str(i.name)] and arr[str(i.name)] > 0:
            num_right_colour = num_right_colour + 1
    games[game]["move"] += 1
    results = check([a,b,c,d],games[game]['answer'])
    return {"num_right_place":results[1],"num_right_colour":results[0],"guess":games[game]["move"]}

def check(guess, answer):
    return sum(min(sum(1 for i in [guess[i] for i in [i for i in range(len(answer)) if guess[i] != answer[i]]] if i == c), sum(1 for i in [answer[i] for i in [i for i in range(len(answer)) if guess[i] != answer[i]]] if i == c)) for c in set(answer)), len(answer) - len([i for i in range(len(answer)) if guess[i] != answer[i]])

def newGameStart():
    return {
        "move":0,
        "answer":[
                str(random.choice(list(Colours)).name),
                str(random.choice(list(Colours)).name),
                str(random.choice(list(Colours)).name),
                str(random.choice(list(Colours)).name)
            ]
    }

def count(arr,a):
    if arr is None:
        arr = {
            str(Colours.a.name): 0,
            str(Colours.b.name): 0,
            str(Colours.c.name): 0,
            str(Colours.d.name): 0,
            str(Colours.e.name): 0,
            str(Colours.f.name): 0,
        }
    arr[a]=arr[a]+1
    return arr
    

class Colours(Enum):
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5