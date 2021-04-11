# RHBot
## Summary
Simple bot to automate combat, selling gear at end of level, and other basic functions. The title of the game this bot is used for will remain hidden until further in the development cycle to reduce the likelihood of a ban. The game in question is an old (>10years since launch) game that is an online multiplayer game on PC.

## Motivation
Alongside the DCW application (specifically the bot playground and creation aspect of DCW), I have an interest in assessing the automation of certain tasks. More specifically I have an interest in the efficiency of automating tasks in comparison to manually doing them. This bot application is intended as a learning experience for useful automation with a reasonably complex set of situations. The approaches to be taken include bot image recognition (probably using OpenCV or similar) and also the standard fixed-sequence movement patterns (using PyAutoGUI and/or PyDirectInput).

## Current Status
* Version 1: Completed
* Version 2: Completed (Partially)
* Version 3: In Progress
* Version 4: Not Started
* Version 5: Not Started

## Plans
### Version 1 - Follower Bot
Will detect the position of the player-controlled character in the same party and move to that character's location.

### Version 2 - Follower Bot with Loot Pickup
Version 1 with the additional ability to detect and pick up all loot objects. Current state of this version is that it can pick up all object it gets a prompt to pick up, but can't navigate independently to faraway loot.

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
3) Automated enemy attack blocking.
4) GPU scaling rather than single CPU core scaling

