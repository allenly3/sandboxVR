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
    "BOARD",
    "DRINK",
    "ARENA",
]
WORD_LENGTH = 5
MAX_GUESSES = 6
CANDIDATE_WORDS = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)


TARGET = ""
COUNTER = 0


# region result check
def _check_wordle_result(guess: str, target_word: str):
    result = [GRAY] * WORD_LENGTH
    target_chars = list(target_word)

    for i in range(WORD_LENGTH):
        if guess[i] == target_word[i]:
            result[i] = GREEN
            target_chars[i] = None

    for i in range(WORD_LENGTH):
        if result[i] == GRAY:
            try:
                idx = target_chars.index(guess[i])
                result[i] = YELLOW
                target_chars[idx] = None
            except ValueError:
                pass

    return tuple(result)


# region validation


def validateCheck(guess):
    global TARGET

    if len(guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be 5 letters.")

    if not guess.isalpha():
        raise HTTPException(status_code=400, detail="Guess must be alphabetic.")

    if TARGET == "":
        raise HTTPException(
            status_code=400, detail="Game not started. Pls Reset Game."
        )
    
    if len(CANDIDATE_WORDS) ==0 :
        raise HTTPException(
            status_code=400, detail="Cannot find Word Pool. Pls Reset Game."
        )

# region API reset
@app.post("/reset")
def resetTarget():
    global TARGET
    global COUNTER
    global CANDIDATE_WORDS
    TARGET = random.choice(WORD_LIST)
    CANDIDATE_WORDS = WORD_LIST.copy()
    COUNTER = 0
    print("For normal mode, target is :", TARGET)
    print("For cheating mode, CANDIDATE_WORDS init length is ", str(len(CANDIDATE_WORDS)))
    return {"status": "201"}


# region API normalguess
@app.post("/normalguess/{guess}")
def handle_normal_guess(guess: str):
    global TARGET
    global COUNTER
    COUNTER += 1

    guess = guess.upper().strip()
    validateCheck(guess)

    colors = _check_wordle_result(guess, TARGET)

    if COUNTER < 6:
        return {"colors": colors, "correct": guess == TARGET, "SECRET_WORD": "*****"}
    else:
        return {"colors": colors, "correct": guess == TARGET, "SECRET_WORD": TARGET}


# region cheating help functions
def _score_pattern(pattern) :
    pass

# region API cheatguess
"""
Keep returning the worst result 
"""

@app.post("/cheatguess/{guess}")
def handle_cheat_guess(guess: str) -> Dict[str, Any]:

    global CANDIDATE_WORDS
    global COUNTER

    guess = guess.upper().strip()
    validateCheck(guess)

    COUNTER += 1
 
    partition = {} 

    for candidate in CANDIDATE_WORDS:
        result_pattern = _check_wordle_result(guess, candidate)
        if result_pattern not in partition:
            partition[result_pattern] = []
        partition[result_pattern].append(candidate)


    print(partition)
