from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import random
import re

app = FastAPI()

"""
API Design:

1. /reset: 
reset TARGET

2. /normalguess/{guess}:  ->  [COLOR] * WORD_LENGTH
return results

3. /cheatguess/{guess}: ->  [COLOR] * WORD_LENGTH:
retunr results

"""

WORD_LIST = [
    "APPLE",
    "TIGER",
    "HOUSE",
    "GRAPE",
    "CHAIR",
    "TABLE",
    "PLANE",
    "SHAKE",
    "OCEAN",
    "SMILE",
    "ACTOR",
    "ANGRY",
    "PROUD",
    "PUNCH",
    "RIGHT",
    "RIVER",
    "SHADE",
    "SOUTH",
    "WATER",
]
WORD_LENGTH = 5
MAX_GUESSES = 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)


TARGET = ""

@app.post("/reset")
def resetTarget():
    global TARGET
    TARGET = random.choice(WORD_LIST)
    return {"status": "201"} 

@app.post("/normalguess/{guess}")
def handle_normal_guess(guess: str) -> Dict[str, Any]:
    pass
