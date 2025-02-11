# Keyboard Overlay App

## Overview
###### MapleStory Keyboard Overlay is a customizable on-screen keyboard display designed for MapleStory players. It helps visualize keybindings, track skill usage, and enhance gameplay efficiency. 

## Features
* Customizable Key Layout – Adjust keys to match your MapleStory key bindings.
* Transparent Overlay – View key presses without obstructing gameplay using OBS.
* Key Press Tracking – Monitor skill usage in real time.

## Instructions 
### How to use with OBS Studio
0. As with all keyboard overlays, BE CAREFUL not to type any sensitive information while the overlay is running.
### Set Up
1. Download this file and save it as overlay.py. Make sure you have "file name extensions" turned on in Windows.
2. Take a screenshot of your key bindings in game using IMPORTANT: 1366x768 resolution and save it AS A PNG FILE. Rename it to bindings.png and save it to the same folder as overlay.py.
3. Install the latest Python version, and add Python to your PATH.
4. Test if Python is installed by running `python --version` (without quotes)
5. Open Command Prompt. Run the command `pip3 install numpy opencv-python pillow pynput` and answer Y to the prompts. This will install dependencies.
### Running the Overlay
6. Run a new Command Prompt AS ADMINISTRATOR*. Step by step: press the Windows key, search for Command Prompt, right click it, click Run as administrator.
7. In the admin Command Prompt, change directory (cd) to the folder that contains overlay.py. For example, if I saved the files to Downloads, I would run the command "cd C:\Users\%USERNAME%\Downloads" (without quotes).
8. In the admin Command Prompt, run the command `python3 overlay.py`.
9. Add the overlay window as a new source in OBS. Use the chroma key filter to remove the green. Resize it to your liking.
###### *Command prompt must be run as administrator to read your key input while you're in the game.