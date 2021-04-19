# RHBot
## Summary
Simple bot to automate combat, selling gear at end of level, and other basic functions. The title of the game this bot is used for will remain hidden until further in the development cycle to reduce the likelihood of a ban. The game in question is an old (>10years since launch) game that is an online multiplayer game on PC.

## Motivation
Alongside the DCW application (specifically the bot playground and creation aspect of DCW), I have an interest in assessing the automation of certain tasks. More specifically I have an interest in the efficiency of automating tasks in comparison to manually doing them. This bot application is intended as a learning experience for useful automation with a reasonably complex set of situations. The approaches to be taken include bot image recognition (probably using OpenCV or similar) and also the standard fixed-sequence movement patterns (using PyAutoGUI and/or PyDirectInput).

## Current Thoughts
The implementation of the V3 combat mode has been difficult due to the size of the changes I am trying to carry out all at once, so there is a lesson learned to implement features piecemeal. Additionally, having the correct decision tree flow has become a difficulty when there are so many possibilities. In future a better plan or graphical method of identifying all possible scenarios is required.

## Current Status
* Version 1: Completed
* Version 2: Completed (Partially - only loots nearby items, sufficient for quests)
* Version 3: In Progress
* Version 4: Not Started
* Version 5: Not Started
* Version 6: Not Started

## Plans
### Version 1 - Follower Bot
Will detect the position of the player-controlled character in the same party and move to that character's location.

### Version 2 - Follower Bot with Loot Pickup
Version 1 with the additional ability to detect and pick up all loot objects. Current state of this version is that it can pick up all object it gets a prompt to pick up, but can't navigate independently to faraway loot.

### Version 3 - Follower Bot with Loot Pickup and Basic Combat
Version 2 with the additional ability to detect when enemies are present and perform basic attacks or combos. Initial version will only work with one ranged class for simplicity but will be updated to allow all 12 classes later. 

### Version 4 - Follower Bot, Loot Pickup, Basic Combat, Stock Movements/Actions in Town
Version 3 with the stock town movements during levelling automated (at least to lvl 10). Will consist of multiple hotkeys for the bot to carry out the stock actions.

### Version 5 - Standalone Bot with Loot Pickup, Full Combat, Single-Level Clear
Taking the loot pickup and combat skills from Version 4 but with an independent navigation system. The idea will be to identify the current area and follow a pre-programmed route through the area either as quickly as possible or as thoroughly as possible.

### Version 6 - Standalone Bot with Loot Pickup, Full Combat, Sell and Repair, Multi-Level Clear
Version 5 with the additional ability to perform the buy/sell actions required at the end of each level, and start another level.

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

