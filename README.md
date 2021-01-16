---
title: README
---

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

## TODO:
* Implement other game modes (in addition to country streak):
	* Hosting battle-royale games
* Make the interface/bot more customizable:
	* Allow changing the prefix more easily
	* Make the program read a config file where things such as the token or path to the driver-executable can be stored
