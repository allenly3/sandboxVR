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
    print(TARGET)
    return {"status": "201"} 

@app.post("/normalguess/{guess}")
def handle_normal_guess(guess: str) -> Dict[str, Any]:
    global TARGET

    guess = guess.upper()

    if len(guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be 5 letters.")

    if not guess.isalpha():
        raise HTTPException(status_code=400, detail="Guess must be alphabetic.")

    if TARGET == "":
        raise HTTPException(status_code=400, detail="Game not started. Call /reset first.")

    colors = [GRAY] * 5
    answer_chars = list(TARGET)

    # check correct
    for i in range(5):
        if guess[i] == TARGET[i]:
            colors[i] = GREEN
            answer_chars[i] = None  # remove matched char

    # present
    for i in range(5):
        if colors[i] == GRAY:
            if guess[i] in answer_chars:
                colors[i] = YELLOW
                answer_chars[answer_chars.index(guess[i])] = None
            else:
                colors[i] = GRAY

    return {
        "colors": colors,
        "correct": guess == TARGET
    }

@app.post("/cheatguess/{guess}")
def handle_normal_guess(guess: str) -> Dict[str, Any]:
    pass
