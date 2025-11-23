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
        raise HTTPException(status_code=400, detail="Game not started. Pls Reset Game.")

    if len(CANDIDATE_WORDS) == 0:
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
    print(
        "For cheating mode, CANDIDATE_WORDS init length is ", str(len(CANDIDATE_WORDS))
    )
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
def _score_pattern(pattern):
    """
    Reason why hits:presents = 4  is because only 5 slots,
    if get 4 presents , players are more likely to win than 1 hit
    so I set ratio hit/present = 4/1
    """
    hits = pattern.count(GREEN)
    presents = pattern.count(YELLOW)

    return (hits * 10) + presents * 2.5


# region API cheatguess
"""
Keep returning the worst result 
"""


@app.post("/cheatguess/{guess}")
def handle_cheat_guess(guess: str):

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

    # print(partition)

    worst_pattern = None
    max_size = -1
    min_score = float("inf")

    for pattern, candidates in partition.items():
        current_score = _score_pattern(pattern)
        current_size = len(candidates)

        # lowest score
        if current_score < min_score:
            min_score = current_score
            worst_pattern = pattern
            max_size = current_size

        # same score, size larger
        elif current_score == min_score:
            if current_size > max_size:
                worst_pattern = pattern
                max_size = current_size

    if not worst_pattern:
        raise HTTPException(
            status_code=500,
            detail="Internal error: No valid partitions found.ReBuild WORD_LIST Pool.",
        )

    # update CANDIDATE_WORDS
    CANDIDATE_WORDS = partition[worst_pattern].copy()

    print(f"After Round {COUNTER},CANDIDATE_WORDS length is {len(CANDIDATE_WORDS)} ")
    colors = list(worst_pattern)
    is_win = worst_pattern == (GREEN, GREEN, GREEN, GREEN, GREEN)

    game_over = is_win or COUNTER >= MAX_GUESSES
    secret_word_reveal = "*****"

    if game_over and not is_win:
        secret_word_reveal = random.choice(CANDIDATE_WORDS)

    return {"colors": colors, "correct": is_win, "SECRET_WORD": secret_word_reveal}
