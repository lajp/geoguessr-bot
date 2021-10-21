**THIS REPOSITORY HAS BEEN ARCHIVED IN THE FAVOUR OF THE [NEW IMPLEMENTATION WRITTEN IN RUST](https://github.com/lajp/geoguessr-bot-rs)**

# geoguessr-bot

This is a simple implementation of a discord bot that sends geoguessr challenge links on demand.

## Requirements:
* 1 geoguessr pro account
* python3
* selenium
* discord.py
* google-chrome
* [chromedriver](https://chromedriver.storage.googleapis.com/index.html)

## Usage:
Launch the bot with:
```bash
python3 main.py
```
On discord simply type `!geo` to receive a country streak challenge without any specific rules

## Rules/Settings:
Rules are specified with appending to the command message a space followed by the setting name and the value separated by a '='

Example with specifying no move:
```
!geo rules=nm
```
Another example with specifying no move, pan or zoom and a time limit of 1 minute (60 seconds)
```
!geo rules=nmpz time=60
```
Starting a battle royale game aka. creating a new lobby:
```
!geo br
```
Specifying a battle royale lobby for the bot to join into to start the game:
```
!geo lobby=[link-to-lobby]
```
Generating a game with a custom/official map:
```
!geo map=[link-to-map]
```
Example with geoguessr official Finland map, 2 min limit and no move:
```
!geo map=https://www.geoguessr.com/maps/finland time=120 rules=nm
```

## TODO:
* Make the interface/bot more customizable:
	* Allow changing the prefix more easily
	* Make the program read a config file where things such as the token or path to the driver-executable can be stored
