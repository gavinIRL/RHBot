# RHBot
## Summary
Simple bot to automate combat, selling gear at end of level, and other basic functions. The title of the game this bot is used for will remain hidden until further in the development cycle to reduce the likelihood of a ban. The game in question is an old (>10years since launch) game that is an online multiplayer game on PC.

## Motivation
Alongside the DCW application (specifically the bot playground and creation aspect of DCW), I have an interest in assessing the automation of certain tasks. More specifically I have an interest in the efficiency of automating tasks in comparison to manually doing them. This bot application is intended as a learning experience for useful automation with a reasonably complex set of situations. The approaches to be taken include bot image recognition (probably using OpenCV or similar) and also the standard fixed-sequence movement patterns (using PyAutoGUI and/or PyDirectInput).

## Current Status
* Version 1: In Progress
* Version 2: Not Started
* Version 3: Not Started
* Version 4: Not Started
* Version 5: Not Started

## Plans
### Version 1 - Follower Bot
Will detect the position of the player-controlled character in the same party and aim to move to that character's location.

### Version 2 - Follower Bot with Loot Pickup
Version 1 with the additional ability to detect and pick up all loot objects.

### Version 3 - Follower Bot with Loot Pickup and Basic Combat
Version 2 with the additional ability to detect when enemies are present and perform basic attacks or combos.

### Version 4 - Standalone Bot with Loot Pickup, Full Combat, Single-Level Clear
Taking the loot pickup and combat skills from Version 3 but with an independent navigation system.

### Version 5 - Standalone Bot with Loot Pickup, Full Combat, Sell and Repair, Multi-Level Clear
Version 4 with the additional ability to perform the buy/sell actions required at the end of each level, and start another level.

## All Other Planned Features
The following are features not explicitly mentioned in the previous section that will be implemented.
### Core Features
1) Target prioritisation.
2) Automated special event handling e.g. bonus areas, special events, etc.

### Additional Features (depending on project progression)
1) General dungeon handler instead of hardcoded for 1 dungeon.
2) Impending enemy attack detection.
4) Automated enemy attack blocking.

## Program Structure
### Multithreading
On the most advanced bots there will be threads for each of the following tasks:
1) Main handling thread: this will decide which threads to start and stop and handle which mode to be in.
2) Screencapture thread(s): this will provide the visual data for the other threads, potential to be GPU accelerated in future.
3) Object detection threads: these will detect enemies, character position, level end, etc.
4) Action thread: this will handle implementation of movement, combat, loot pickup, etc.
### Modes
On the most advanced bots there will be multiple modes (in order to limit processor resource draw)
1) Movement mode: this will be the lightest mode that will have low frequency loot checking and very low frequency enemy detection.
2) Combat mode: this will include high frequency enemy detection, high frequency enemy prioritisation, and no loot detection.
3) Single enemy combat mode: this will include high frequency enemy detection, no enemy prioritisation, and no loot detection.
4) Loot mode: this will include high frequency loot detection and low frequency enemy detection.
### Object Detection
In each detection category the following objects will be the target images:
* TBC
