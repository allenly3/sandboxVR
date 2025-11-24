**BUILD AND RUN**
- Make Sure Your Device having Python 3.12.2 or higher installed
- Run 'run.bat'
<img width="241" height="372" alt="image" src="https://github.com/user-attachments/assets/32ef32d4-a541-42af-8978-55e20dff294a" />



**TEST WAY**
- For Local game ( Task1 and Task4), you will see the SECRET_WORD in the cmd window when you run 'run.bat'
<img width="1098" height="630" alt="{80CBF455-5AF7-4822-ABBE-14B1EA535404}" src="https://github.com/user-attachments/assets/25a129b5-c3fd-407c-9a72-63b0f6ba3e2e" />

- For Online Mode (Task2 and Task3), **GUESS BY YOURSELF**
  OR run the backend manually instead runnng 'run.bat', like switch to backend folder, cmd
  run server "**uvicorn server:app --reload --port 8000**"
  And you will see the "**Normal mode**'s SECRET_WORD like:
  <img width="1079" height="323" alt="{E001666B-EDBD-4870-AD94-22C3181E855A}" src="https://github.com/user-attachments/assets/154792aa-5e59-4483-b446-484fc8d608c2" />

  For **Cheat mode**, no way to get it until end. BUT you can type "AEIOU", **all Vowels**, 
  and the CANDIDATES_WORD length becomes one , which is "PUNCH"

<img width="779" height="89" alt="{4229B3A6-46BE-45B9-85A3-7F22FC30E546}" src="https://github.com/user-attachments/assets/20487594-0531-4be4-9677-3938c3c70929" />


**GAME DESIGN**
<img width="1038" height="730" alt="{F8160217-55C5-4683-A718-DAC807522094}" src="https://github.com/user-attachments/assets/11c71110-7b7f-449a-ac12-510dad9e43f8" />




**DOCUMENTATION**
1. Project Overview
    
    This is the Sandbox VR Wordle Task.
    
    This game is written by Python 3.12.2, both front-end and back-end. 
    
    (I was trying to use Unity or Cocos, but for this worde game, those Game Engines are too heavy.
    So Finally decicded using pygame.)
    
    The game Menu has 3 modes,  single Mode(**task1**) , Online Mode and PVP Mode(2 player competing, **task4**).
    
    And in Online Mode, players can choose "Normal"(**task2**) or "Cheat"(**task3**), 
    and guessing result will be decided by the server under online Mode.
    
<img width="1008" height="627" alt="{9F48F890-E1C1-43AB-926E-4E74DF1ECCEB}" src="https://github.com/user-attachments/assets/565a347d-48d2-471a-bd74-809aa46c2f0f" />




2. Key Features
    - Players can play any mode without recompilation. 
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
<img width="1003" height="633" alt="{69FD6CB7-2749-47C4-B0BB-98354311E972}" src="https://github.com/user-attachments/assets/de187f74-b131-4edb-8cbb-63d94a637925" />

    
    


3. Bonus Features:
    - Add Game Sound effects
    - Game Theme style is same as SandboxVR.com, like color, app logo, etc
    <img width="1000" height="48" alt="{EE5F9D87-635A-44A5-9817-7F9AAC39DA2E}" src="https://github.com/user-attachments/assets/61124faf-0d14-4e3a-a8f1-896b067a251f" />
    <img width="1000" height="835" alt="{45517037-3F6F-4A57-B6C6-1DD20185C997}" src="https://github.com/user-attachments/assets/d133da53-5c69-43ad-9ca9-895b3d3d057a" />

    - Framework is light weight
    - PVP mode doesnt show guessing letter until both players finish same round
    - run 'run.bat' to play game directly


4. Improvements / TODO List:
    - Add winning Animation
    - Countdown clock for entering guessing
    - PVP game add more than 2 people, and can group up 
    - Separate Interface in PVP, players can entering guessing at the same time
    - Add error handling class, like popup Msg
    - All four modes set SECRET_WORD from online source
    - Record log


5. Tech Stack
    - Language: Python
    - Backend: Python 3.12.2, FastAPI, Uvicorn, API Endpoints
        /reset
        /normalguess/{guess}
        /cheatguess/{guess}

    - Frontend: Python 3.12.2, Pygame
        In Game Logic.

    - Deployment: Docker, Bash

