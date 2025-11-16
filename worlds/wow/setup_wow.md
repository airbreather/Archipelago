# Setup WoW Archipelago World

This is a tutorial file for the World of Warcraft Archipelago integration.  

## Requirements
- A working AzerothCore server with Azeroth Lua Engine (mod-ale).
- A copy of the old World of Warcraft: Wrath of the Lich King 3.3.5a client.
- The provided lua scripts placed in `lua_scripts/`.
- The `json.lua` file.
- Node.js and node package manager (npm) installed.
- The Node.js bridge (`arch_bridge.js`) running on `localhost:3000`.

## First-Time Setup Guide
- Follow the steps in the AzerothCore Classic Installation Guide. Make sure it runs correctly.
- Follow the instructions to install mod-ale. Make sure it still runs correctly.
- Place the provided lua files in azerothcore-wotlk/build/bin/RelWithDebInfo/lua_scripts.
- Download the `json.lua` file from https://github.com/rxi/json.lua and place it with the rest of the lua_scripts.
- Extract the ap-bridge file and place it somewhere safe. 
- Use terminal (Mac) or Node.js command prompt (Windows) to navigate to the ap-bridge directory.
- Run `npm install` to install required files.
- Launch the AzerothCore servers (`authserver.exe` and `worldserver.exe`).
- If it successfully runs with no errors, delete the `ap_vendor.lua` file.

## Launch the Game
- Add the per-game `AP_ItemIds.lua` and `AP_LocationIds.lua` to `lua_scripts`. Overwrite any previous copies.
- If there is a data folder in the lua_scripts directory, delete all files within.
- Make sure the AzerothCore servers are running.
- Launch the WoW 3.3.5a Client. Log in to the account that was made while installing AzerothCore.
- Create a character matching the options chosen in the yaml.
- In the terminal at the arch_bridge location, run `node arch_bridge.js` to start the bridge.
- Once in game, type ` !connect url slotname password` or ` !connect url slotname` with the appropriate url and password. Make sure to include the leading whitespace.
- Progress in WoW (leveling up, questing, buying spells) to send Archipelago location checks.
