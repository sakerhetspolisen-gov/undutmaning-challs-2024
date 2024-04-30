from contextlib import nullcontext
from os import replace,urandom
from base64 import b64encode
from typing import Union
from xml.etree.ElementTree import tostring
import uvicorn
import string
import  random
import json
import hashlib
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import ssl
import base64
import math

app = FastAPI()
#app.add_middleware(HTTPSRedirectMiddleware)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('cert.pem', keyfile='key.pem')

TheFlag = "undut{ThisIsTheFlag}"


challengecode = ""


challcode = []
player_positions = []
computer_positions = []
initial_reply = {"player_positions" : player_positions,
         "computer_positions" : computer_positions,
         "challenge" : challcode}

letters = ["A","B","C","D"]
numbers = []
for x in range(1,10):
    numbers.append(x)

cords = []
for letter in letters:
    for number in numbers:
        cords.append(letter + str(number))




reply = {"Hit" : False,
         "Countermove": "A0",
         "GameStatus" : "Game Status: Playing!",
         "Flag" : "Flag: Win the game you must!",
         "player_positions" : player_positions,
         "computer_positions" : computer_positions,
         "challenge" : challcode}
         


#def create_challcode(randstring):
    #return 
    

def create_challenge_code():
    challcode.clear()    
  

    randstring = ""
    randcords = player_positions + computer_positions
    for cord in randcords:
        randstring += cord
    
    result_str = ''.join(random.choice(randstring) for i in range(2))
    
    global challengecode
    challengecode = result_str

    b64chall = base64.b64encode(result_str.encode()).decode()

    challcode.append(b64chall)


def check_chall_code(chall_resp_b64, target_cord):
    
    try:
        chall_resp = base64.b64decode(chall_resp_b64.encode())
    except:
        raise Exception ("not base64")
    
    try:
        cord = xor(chall_resp,challengecode.encode())
    except Exception as msg:
        raise Exception ("xor failed")

    if(cord == target_cord[::-1].encode()):
        return True
    else:
        return False
    

def xor(key,data):
    try:
        if len(key) < len(data):
            localkey = key * math.ceil(len(data) / len(key))
        else:
            localkey = key
    except Exception as msg:
        raise Exception ("xor failed")
    
    return bytearray(a ^ b for a, b in zip(*map(bytearray, [data, localkey])))



@app.get("/")
def read_root():
    return "This is not the base you are looking for"


@app.get("/new_game/")
def read_item():
    player_positions.clear()
    computer_positions.clear()

    tempplayer_positions = random.sample(cords, 5)
    tempcomputer_positions = random.sample(cords, 5)
    
    for pos in tempplayer_positions:
        player_positions.append(pos)
    
    for pos in tempcomputer_positions:
        computer_positions.append(pos)

    create_challenge_code()
    
    
     
    return initial_reply


@app.get("/shoot/")
def read_item(cord: str,chall_resp: str):
    
    try:
        if(check_chall_code(chall_resp,cord)):
            print("challenge pass")
        else:
            return 418
    except Exception as msg:
        return repr(msg), 400
    
    if cord.upper() in computer_positions:
        computer_positions.remove(cord.upper())
        reply["Hit"] = True
        
    else:
        reply["Hit"] = False

    
    reply["Countermove"] = player_positions.pop()
    
    if len(player_positions) > 0:
        
        reply["GameStatus"] = "Game Status: Playing!"
    else:
        reply["GameStatus"] = "Game Status: Game Over!"
    
    if len(computer_positions) == 0:
        reply["GameStatus"] = "Game Status: You win! sort of..."
        reply["Flag"] = TheFlag
    return reply



if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem",ssl_certfile="cert.pem")          
    uvicorn.run(app, host="0.0.0.0", port=8000)