# Hemonaluto
**A text adventure game**

Hemonaluto is a text based adventure game where you wake up in a curious magical world with a dark and powerful secret.

The story isn't developed yet, so far there are only three rooms to discover.

## How it works

### Developers
Windows:

1. Open terminal as administrator.
2. Run ```winget install GnuWin32.Make```
3. Run ```setx /M path "%path%;C:\Program Files (x86)\GnuWin32\bin"```

Windows and Linux:

4. Navigate to the folder you want to clone the project to.
5. Run ```git clone https://github.com/hemonaluto/Hemonaluto.git```
6. Happy coding!

### Players

1. Open terminal as administrator.
2. Run ```pip install hemonaluto```
3. Run ```hemonaluto```

You are welcomed and prompted to type in a command. This command should be written from the perspective of the player, similar to how you would play in the game Zork. 

## Contributors
### How you can help
If you want to improve this game, fix bugs, write tests or add documentation, please feel free to do so, any kind of contribution is welcome. Simply open an issue and submit a pull request so we can discuss and close it.

To create your custom world or change the existing one you can edit ```scripts/world_generation.py``` and run ```make generate_world```.

## Commands
### quit/q/exit
This command quits the game entirely.
### examine/look/l
Examine any kind of in-game element. Type the thing you want to examine after the command, e.g. examine door, or don't and get a general description of your environment.
### north/northeast/n/up/u/...
Move in desired direction.
### open/unlock
Unlock a door or chest.
### get/take/pick
Take an item.
### inventory/i
List all the items in your inventory.
### save/load
Save or load your game state.
### restart
Restart the game.
### score
View your score.
### diagnostic/health
View your current health.
### throw at
Throw any item at whatever target you choose.
### close
Close a door or chest.
### read
Read an items engraved or written on text.
### drop
Drop an item.
### put
Put an item in or on another item.
### press/turn
Use a button or valve.
### move/push/pull
Move an object to reveal what is underneath it.
### attack with/kill with
Attack an entity with your specified weapon.
### eat/drink
Eat or drink something to replenish health.
### tie/attach
Tie or attach a rope to something.
### destroy/break
Break a breakable item.
### listen
Listen to your surroundings.
### smell
Smell your environment.
### hide in/under
Hide in or under something
### leave/appear
Leave your hiding spot.