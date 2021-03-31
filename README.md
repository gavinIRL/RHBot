# RHBot
## Summary
Simple bot to automate combat, selling gear at end of level, and other basic functions. The title of the game this bot is used for will remain hidden until further in the development cycle to reduce the likelihood of a ban. The game in question is an old (>10years since launch) game that is an online multiplayer game on PC.

## Motivation
Alongside the DCW application (specifically the bot playground and creation aspect of DCW), I have an interest in assessing the automation of certain tasks. More specifically I have an interest in the efficiency of automating tasks in comparison to manually doing them. This bot application is intended as a learning experience for useful automation with a reasonably complex set of situations. The approaches to be taken include bot image recognition (probably using OpenCV or similar) and also the standard fixed-sequence movement patterns (using PyAutoGUI and/or PyDirectInput).

## Current Status
Version 1: In Progress
Version 2: Not Started
Version 3: Not Started
Version 4: Not Started

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

## All Planned Features (Section will be removed soon and replaced by versions subsections in Plans)
1) Automated movement to next area
2) Automated basic combat, enemy detection, and target prioritising
3) Automated loot pickup
4) Automated selling of loot
5) Automated special event handling (bonus areas, etc.)
6) Multiple levels/zones
7) More advanced combat e.g. impending enemy attack detection, automated blocking
