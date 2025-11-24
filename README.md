BUILD AND RUN



GAME DESIGN


DOCUMENTATION
1. Project Overview
    This is the Sandbox VR Wordle Task.
    
    This game is written by Python 3.12.2, both front-end and back-end. 
    
    (I was trying to use Unity or Cocos, but for this worde game, those Game Engines are too heavy.
    So Finally decicded using pygame.)
    
    The game Menu has 3 modes,  single Mode(task1) , Online Mode and PVP Mode(2 player competing, task4).
    
    And in Online Mode, players can choose "Normal"(task2) or "Cheat"(task3), 
    and guessing result will be decided by the server under online Mode.



3. Key Features
    - **Task1**: Pure local game, 5-letter long word, max 6 chance to guess to win. 
    - **Task2** & **Task3**: 
        Online mode, server will validate the input, and decides SECRET_WORD.  
        Front-end will recieve "*****" as SECRET_WORD until gameover or guessing correct. 
        
        **Task2**, Normal mode, sending API: {API_BASE_URL}/**normalguess**/{word}
        
        **Task3**, Cheat mode, sending API: {API_BASE_URL}/**cheatguess**/{word}
            For cheat mode, there is a function to calculate guessing score, 
            I optmized the score, because the game only has 5 slots,
            if get 4 presents , players are more likely to win than 1 hit
            so I set ratio socre of **hit/present =  4/1**

        Both tasks are using {API_BASE_URL}/reset to reset game status
        In online mode,  once game starts, player cannot switch mode until game over or replay game. 

    - **Task 4**, its PVP mode, 2 players compete each other. 
        Highlight designs are :
                * The first entring player is random
                * Two players take turns inputting guessing
                * Only both players finish guessing lines show guessing letter+color, otherwise only show guessing color

    
    - Players can play any mode without recompilation. 


4. Bonus Features:
    - Add Game Sound effects
    - Game Theme style is same as SandboxVR.com, like color, app logo, etc
    - Framework is light weight
    - PVP mode doesnt show guessing letter until both players finish same round


5. Improvements / TODO List:
    - Add winning Animation
    - Countdown clock for entering guessing
    - PVP game add more than 2 people, and can group up 
    - Separate Interface in PVP, players can entering guessing at the same time
    - Add error handling class, like popup Msg
    - All four modes set SECRET_WORD from online source


6. Tech Stack
    - Backend: Python 3.12.2, FastAPI, Uvicorn, API Endpoints
        /reset
        /normalguess/{guess}
        /cheatguess/{guess}

    - Frontend: Python 3.12.2, Pygame
        In Game Logic.

    - Deployment: Docker

