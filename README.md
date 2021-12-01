
# Introduction

Geometronome Dash is an adaptation of “Geometry Dash”, along with some additional features. Geometronome Dash works very similarly to Geometry Dash, in that you have a square that clears obstacles according to the rhythm of the music. Geometronome Dash aims to recreate that while still allowing the player to input any music file they like. After which, the game will use a beat-detection, pitch-detection, and smart map generation algorithm to generate the obstacles according to the rhythm and intensity of the music. The frequency of obstacle generation will utilize beat-detection algorithms while the complexity of the map will depend on the loudness and pitch of the music at that particular point of the music.

# Installation Instructions

In order to run the project, the following modules must first be downloaded:

### cmu_112_graphics

From: https://www.cs.cmu.edu/~112/notes/notes-graphics.html

For Windows:
1. Run this Python code block in your main Python file (it will print the commands you need to paste into your command prompt):
'''
import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')
'''
2. Open Command Prompt as an administrator user (right click - run as administrator)
3. Copy-paste each of the two commands printed in step 1 into the command prompt you opened in step 2.
4. Close the command prompt and close Python.
5. Re-open Python, and you're set (hopefully)!

For Mac or Linux
1. Run this Python code block in your main Python file (it will print the commands you need to paste into your command prompt):
import sys
print(f'sudo "{sys.executable}" -m pip install pillow')
print(f'sudo "{sys.executable}" -m pip install requests')
2. Open Terminal
3. Copy-paste each of the two commands printed in step 1 into the command prompt you opened in step 2.
- If you see a lock and a password is requested, type in the same password that you use to log into your computer.
4. Close the terminal and close Python.
5. Re-open Python, and you're set (hopefully)!

### numpy
'''
pip install numpy
'''

### Pygame
'''
pip install pygame
'''

### PyAudio
'''
pip install PyAudio
'''

### Aubio
'''
pip install aubio
'''

### PyWavelet
'''
pip install PyWavelet
'''

### Scipy
'''
pip install scipy
'''

### Wave
'''
pip install Wave
'''

# Run Instructions

1. In order to run the code, run main.py

# List of Shortcuts for the game
