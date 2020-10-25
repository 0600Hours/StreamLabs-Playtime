# About
Steam Playtime fetches info about a game in your library and sends a chat message letting people know how long you've played the game.

# Setting Information

## General

### Command Name
The Command Name setting controls how users will call this command. It is recommended but not required to start with a "!"

### Message
The Message setting specifies the chat message format
- {channel_name} will be replaced with your channel's name
- {time_played} will be replaced with how long you've played the game, with a unit as specified by the Time Unit setting
- {game_name} will be replaced with the name of the game as specified by the Game Name setting

### Time Unit
The Time Unit setting controls how your playtime will be displayed. You can choose between Minutes, Hours, and Days.
This unit is automatically converted and displayed in the Message setting, wherever you include {time_played} in the message

### Cooldown
The Cooldown setting controls the minimum time elapsed before a user can call the command again.
Warning: If set too low, you may end up being rate limited by Steam.

## Game Settings

### Game Name
The Game Name setting controls how the game will be named in the Message setting. It is recommended to be the same as the name as displayed on Steam, but not required.

### Game ID
The Game ID setting is what actually controls the game that is requested from steam.
You can find this using https://steamdb.info/ by searching for your game and entering the value that appears under "App ID"

## Steam

### Steam ID
The Steam ID setting controls for which account the command will fetch information.
You can find this using https://steamidfinder.com/ by searching for yourself and entering the value that appears under "steamID64"

### Steam API Key
The Steam API Key setting is necessary for the command to function.
You can create an API Key by navigating to https://steamcommunity.com/dev/apikey