# RHBot
## Summary
Simple bot to automate combat, follow other players, and pick up loot. The title of the game this bot is used for will remain hidden until further in the development cycle to reduce the likelihood of a ban. The game in question is an old (>10years since launch) game that is an online multiplayer game on PC.

## Current Thoughts
Currently working on the multi-bot manual control in https://github.com/gavinIRL/RHBotArray. Plan to test in the RHBot repo before separating the user "client" from the bot "server" and holding in separate repos. The RHBot will be the server and the RHBotArray will be the client and possibly renamed to RHBotController.

## Current Status
* Version 1: Completed
* Version 2: Completed (Partially - only loots nearby items, sufficient for quests)
* Version 3: Completed (Support only for 1 class, Version 3.1 includes hotkeys)
* Version 4: Completed (Partially - includes recordings for first 10 levels)
* Version 5: In Progress (See https://github.com/gavinIRL/RHBotArray)
* Version 6: Not Started
* Version 7: Not Started
* Version 8: Not Started

## Plans
### Version 1 - Follower Bot
Will detect the position of the player-controlled character in the same party and move to that character's location.

### Version 2 - Follower Bot with Loot Pickup
Version 1 with the additional ability to detect and pick up all loot objects. Current state of this version is that it can pick up all object it gets a prompt to pick up, but can't navigate independently to faraway loot.

### Version 3 - Follower Bot with Loot Pickup and Basic Combat
Version 2 with the additional ability to detect when enemies are present and perform basic attacks or combos. Initial version will only work with one ranged class for simplicity but will be updated to allow all 12 classes later. 

### Version 4 - Follower Bot, Loot Pickup, Basic Combat, Stock Movements/Actions in Town
Version 3 with the stock town movements during levelling automated (at least to lvl 10). Will consist of multiple hotkeys for the bot to carry out the stock actions. Plan to integrate into the existing bot rather than having an additional bot. Aim to have it running on main pc also for quick record and distribute purposes.

### Version 5 - Follower Bot, Loot Pickup, Basic Combat, Town Movements through Socket from Primary User
Version 4 with an alternative method of communication to the bots from the primary user, will allow a single set of inputs/actions to be sent to all connected bots. More flexible than record->distribute->play used in Version 4.

### Version 6 - Follower Bot, Loot Pickup, Basic Combat, Town Movements through Socket from Primary User, Automatic Sell and Repair
Version 5 with the ability for the bots to automatically sell all (useless) loot and repair all gear at end of a level.

### Version 7 - Standalone Bot with Single-Level Clear
Taking all of the features from Version 6 but with an independent navigation system. The idea will be to identify the current area and follow a pre-programmed route through the area either as quickly as possible or as thoroughly as possible. Will clear a level and then wait for the user to either choose a new

### Version 8 - Standalone Bot with Loot Pickup, Full Combat, Multi-Level Clear
Version 7 with the additional ability to perform the buy/sell actions required at the end of each level, and start another level.

## All Other Planned Features
The following are features not explicitly mentioned in the previous section that will be implemented.
### Core Features
1) Target prioritisation.
2) Automated special event handling e.g. bonus areas, special events, etc.

### Additional Features (depending on project progression)
1) General dungeon handler instead of hardcoded for 1 dungeon.
2) Impending enemy attack detection.
3) Automated enemy attack blocking.
4) GPU scaling rather than single CPU core scaling (not necessarily required as get 10-100fps on the bot most of the time)

