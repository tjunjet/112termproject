# Importing the standard Python Libraries
from cmu_112_graphics import *
import random
import math
import os
import time
import pygame
import numpy as np

# ------------------------------------------------------------------------------
#                           IMPORTING MY OWN LIBRARIES
# ------------------------------------------------------------------------------

import shapes
import bpm_detection
import sound
import pitch_detection
import audio_length

# Directions

NORTH = (0, -5)
SOUTH = (0, 5)
EAST = (5, 0)
WEST = (-5, 0)
NORTH_EAST = (5, -5)
NORTH_WEST = (-5, -5)
SOUTH_EAST = (5, 5)
SOUTH_WEST = (-5, 5)

directions = [NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST]

# ------------------------------------------------------------------------------
#                               MODEL: appStarted
# ------------------------------------------------------------------------------

def appStarted(app):
    app.mode = "splashScreenMode"
    app.modesList = ['gameMode', 'reverseGravityMode', 'zigZagMode']
    app.filename = "Music/Forever Bound - Stereo Madness.wav"
    app.songname = ""
    restartGame(app)

# Making a function to restart game
def restartGame(app):
    booleanOptions(app)
    soundOptions(app)
    timerOptions(app)
    graphicOptions(app)
    imageOptions(app)
    obstacleOptions(app)
    scoreOptions(app)
    pitchOptions(app)
    logicOptions(app)

# Boolean options
def booleanOptions(app):
    app.modesDict = {'gameMode': [0, 0, 255], 'reverseGravityMode': [255, 0, 0], 
                 'zigZagMode': [255, 255, 0]}
    app.height = 400
    app.width = 700
    app.ground = (0, app.width, app.height * 0.75, app.height * 0.75)
    app.ceiling = (0, app.width, int(app.height * 0.25), int(app.height * 0.25))
    app.magicSquare = shapes.magicSquare(30, 30, "green", 
                       app.width / 5 + 10 , app.ground[2] - 15)
    app.isInAir = False
    app.shapes = []

    # List of obstacles that the magic square has not passed
    # Once the magic square clears the obstacle, we will remove the obstacle
    app.obstacles = []
    app.gameover = False

    # Calculating distance between magicSquare and right bound of app
    app.squareWidthDistance = app.width - app.magicSquare.x1

    # Speed at which obstacle is approaching the magicSquare
    # Formula for speed = no. of pixels travelled / second
    # Since every second, we move to the left by 5 pixels, the obstacleSpeed is
    # calculated as such: 
    app.obstacleSpeed = 5 / app.timerDelay

    # Hence, the time taken for the obstacle to travel from the width to the
    # magic square = app.squareWidthDistance / app.obstacleSpeed
    # This is needed so that the magicSquare can jump is pressed according to 
    app.timeDelayed = app.squareWidthDistance / app.obstacleSpeed
    # Changes to true the moment the delay has ended.
    # app.timeDelayedInitialized = False

    # Checking if the magicSquare is on a square
    app.isOnSquare = False

    # Checking if square is currently dropping or flying
    app.isDropping = False

    # Getting the height of a square
    app.squareHeightScale = 1
    app.scaleAscending = True

    # Initializing a randomized obstacleID
    app.obstacleID = 1

    # Checking if the square is in the portal
    app.isOnPortal = False

# Checking the logic
def logicOptions(app):
    app.playButtonBig = False
    app.mapPackBig = False
    app.highScoreBig = False
    app.backButtonBig = False
    app.replayButtonBig = False
    app.returnHomeBig = False

# Drawing imageOptions
def imageOptions(app):
    # Creating images for the splash screen
    # From: https://gdbrowser.com/
    app.splashScreenBackground = app.loadImage("Images/geometry_dash_background.jpeg")
    app.splashScreenLogo = app.loadImage("Images/geometry-dash-logo.png")
    # Play Button
    # From: https://picsart.com/i/295292011008211
    app.splashScreenPlayButton = app.loadImage("Images/geometry_dash_play_button.png")
    app.splashScreenPlaySmallButton = app.scaleImage(app.splashScreenPlayButton, 2/3)
    # High Scores and scaled
    # https://gdbrowser.com/
    app.highScoreImage = app.loadImage("Images/high_scores.png")
    app.highScoreSmallImage = app.scaleImage(app.highScoreImage, 1/2)
    # Map pack image and scaled
    # https://gdbrowser.com/
    app.mapPackImage = app.loadImage("Images/map_packs.png")
    app.mapPackSmallImage = app.scaleImage(app.mapPackImage, 1/2)
    # Back button
    # From: https://www.iconfinder.com/icons/2454800/arrow_direction_go_back_send_button_icon
    app.backButton = app.loadImage("Images/back_button.png")
    app.backSmallButton = app.scaleImage(app.backButton, 0.1)
    # Game over image
    # From: https://coolwallpapers.me/2605119-minimalism.html
    app.gameOverImage = app.loadImage("Images/game_over.png")
    app.smallGameOverImage = app.scaleImage(app.gameOverImage, 0.1)
    # Replay button image
    # From: https://cutewallpaper.org/21/geometry-dash-pic/view-page-21.html
    app.replayButton = app.loadImage("Images/replay_button.png")
    app.smallReplayButton = app.scaleImage(app.replayButton, 0.5)
    app.mediumReplayButton = app.scaleImage(app.smallReplayButton, 1.4)
    # Return to home button
    # From: https://twitter.com/therealgdcolon/status/1362503200713166849
    app.returnToHomeButton = app.loadImage("Images/homeButton.png")
    app.smallHomeButton = app.scaleImage(app.returnToHomeButton, 0.4)
    app.mediumHomeButton = app.scaleImage(app.smallHomeButton, 1.4)
    # Portal Image
    # From: https://geometry-dash.fandom.com/wiki/Portals
    app.portalImage = app.loadImage("Images/portal.png")
    app.smallPortalImage = app.scaleImage(app.portalImage, 0.25)
    # Congratulations Image
    # From: https://insights.dice.com/2018/08/15/hyper-casual-games-explained/
    app.congratulationsImage = app.loadImage("Images/congratulations.png")
    app.smallCongratsImage = app.scaleImage(app.congratulationsImage, 0.4)
    # Paused Image
    # From: https://www.shutterstock.com/video/clip-14307913-pause-grunge-retro-video-game--tv
    app.pausedImage = app.loadImage("Images/paused.png")
    app.smallPausedImage = app.scaleImage(app.pausedImage, 0.5)
    # Pause Button
    # From: https://thepngstock.com/image/isometric-shoping-bucket
    app.pauseButton = app.loadImage("Images/pause_button.png")
    app.smallPauseButton = app.scaleImage(app.pauseButton, 0.18)

def obstacleOptions(app):
    return

# Graphics parameters
def graphicOptions(app):
    # Creating the shapes for the splash mode
    app.splashShapeList = []

    # Generating background color
    # Note that this color changes every time the mode changes
    app.backgroundColor = [0, 0, 255]
    app.isIncreasing = True

# Function that contains all the sound parameters
def soundOptions(app):
    pygame.mixer.init()
    # Getting the filename of splash screen music
    # https://www.youtube.com/watch?v=qG3wCA4L7Aw
    app.splashScreenMusicFile = "Music/Geometry Dash OST _ Title Screen (Menu Loop).wav"
    app.splashScreenMusic = sound.Sound(app.splashScreenMusicFile)
    app.splashScreenMusic.start()
    app.gameMusic = None
    # Getting the filename of the game song
    # https://www.youtube.com/watch?v=JhKyKEDxo8Q
    # Gets the beat per minute of the song
    app.bpm = bpm_detection.getBPM(app.filename)
    # Getting the parameters to play song when the game starts
    # Period let's us know the time interval in which obstacles appear
    # Using the physics equation f = 1 / T
    # Frequency is the number of beats per minute (By definition of frequency)
    # Period: Defined as the time interval between successive beats
    # For now, I multiply 4 to period for simplicity
    app.period = 4 * 60 / app.bpm
    # Getting the list of pitches in the music
    app.pitches = pitch_detection.getListOfPitches(app.filename)
    # Getting the length of the pitches
    app.pitchesLength = len(app.pitches)
    # Initializing the pitch index depending on the duration of the song
    app.pitchIndex = 0
    # Getting the duration of the music
    app.duration = audio_length.getDurationOfMusic(app.filename)
    # Frequency of sampling the app.pitches
    app.samplingFrequency = app.duration / app.pitchesLength
    app.calculateParams = True

def pitchOptions(app):
    app.pitchOne = np.percentile(app.pitches, 25)
    app.pitchTwo = np.percentile(app.pitches, 75)

# Function that contains anything related to timerFired
def timerOptions(app):
    app.timerDelay = 20
    app.timeElapsed = 0
    # Getting the startTime so it is easier to compute BPM
    app.startTime = 0
    app.realStartTime = 0
    # Time Options
    app.tempTimePassed = 0
    app.startTimeOne = 0

# Function that contains anything related to scoring
def scoreOptions(app):
    app.score = 0

# ------------------------------------------------------------------------------
#                               PROCESSING MUSIC
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#                            VIEW: DRAWING FUNCTIONS
# ------------------------------------------------------------------------------

# Drawing the portal
def drawPortal(app, canvas, cx, cy):
    canvas.create_image(cx, cy, image = ImageTk.PhotoImage(app.smallPortalImage))

# Getting random color
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

# Changing the background color gradually
def changeBackgroundColorGradually(app):
    # Changing the gameMode's color
    if app.isIncreasing == True:
        if app.backgroundColor[0] == 255:
            app.isIncreasing = False
        else:
            app.backgroundColor[0] += 1
    else:
        if app.backgroundColor[0] == 0:
            app.isIncreasing = True
        else:
            app.backgroundColor[0] -= 1


# Drawing the percentage score
def drawScore(app, canvas):
    canvas.create_text(app.width / 2, 30, text = f"Score: {app.score} %", font = "Arial 26 bold")

# Drawing the background
def drawBackground(app, canvas):
    color = rgbString(app.backgroundColor[0], app.backgroundColor[1], app.backgroundColor[2])
    canvas.create_rectangle(0, 0, app.width, app.height, fill = color)

# Drawing the magic square
def drawMagicSquare(app, canvas):
    x0 = app.magicSquare.x0
    x1 = app.magicSquare.x1
    y0 = app.magicSquare.y0
    y1 = app.magicSquare.y1
    canvas.create_rectangle(x0, y0, x1, y1, fill = "green", width = "3")

# Drawing the triangle obstacle
def drawTriangle(app, canvas, x0, y0, x1, y1, x2, y2, color):
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill = color, width = "10")

# Drawing the square obstacle
def drawSquare(app, canvas, x0, y0, x1, y1, color):
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = "3")

# Drawing the rectangle obstacle
def drawRectangle(app, canvas, x0, y0, x1, y1, color):
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = "3")

# Drawing a mountain obstacle
def drawMountain(app, canvas, x0, y0, x1, y1, x2, y2, color):
    canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill = color)

# Drawing the ground. This does not change throughout the game for now.
def drawGround(app, canvas):
    x0, x1, y0, y1 = app.ground
    canvas.create_line(x0, y0, x1, y1, fill = "black", width = "10")

# Drawing the ceiling.
def drawCeiling(app, canvas):
    x0, x1, y0, y1 = app.ceiling
    canvas.create_line(x0, y0, x1, y1, fill = "black", width = "10")

# Loop through the list of obstacles and draw them
def drawObstacles(app, canvas):
    for obstacle in app.obstacles:
        # If it is a triangle, we draw a polygon in the shape of a triangle
        if isinstance(obstacle, shapes.Triangle):
            drawTriangle(app, canvas, 
                        obstacle.x0, obstacle.y0,
                        obstacle.x1, obstacle.y1,
                        obstacle.x2, obstacle.y2,
                        "orange")

        # If it is a square, we draw a square
        elif isinstance(obstacle, shapes.Square):
            drawSquare(app, canvas, 
                       obstacle.x0, obstacle.y0,
                       obstacle.x1, obstacle.y1, "purple")

        # If it is a portal, we draw circle
        elif isinstance(obstacle, shapes.Portal):
            drawPortal(app, canvas, obstacle.cx, obstacle.cy)

        # If it is a rectangle, we draw rectangle:
        elif isinstance(obstacle, shapes.Rectangle):
            drawRectangle(app, canvas, 
                          obstacle.x0, obstacle.y0, 
                          obstacle.x1, obstacle.y1, "cyan")

        # If it is a mountain, we draw the mountain
        elif isinstance(obstacle, shapes.Mountain):
            drawMountain(app, canvas, 
                        obstacle.x0, obstacle.y0,
                        obstacle.x1, obstacle.y1,
                        obstacle.x2, obstacle.y2,
                        obstacle.color)


# ------------------------------------------------------------------------------
#                              CONTROLLER FUNCTIONS
# ------------------------------------------------------------------------------

# Function to add obstacles randomly based on the BPM

def addObstacle(app):
    # Every 10% of the song, we generate a portal
    if app.score % 10 == 0 and app.score != 0:
        # Draw a portal if this happens
        # app.obstacles.append(portal)
        portal = shapes.Portal(app.width, app.height * 0.75 - 20)
        app.obstacles.append(portal)

    # Creating obstacles for gameMode
    elif app.mode == "gameMode":
        # Here, we will perform some smart, random generation on the obstacles
        # Using pitches 
        # Adding the obstacles based on the frequency of pitches
        # if 0 <= app.pitches[app.pitchIndex] < 20:
        #     app.obstacleID = 1

        # elif app.pitches[app.pitchIndex] > 40:
        #     app.obstacleID = 2

        # else:
        #     app.obstacleID = random.randint(1, 2)

    # Creating triangle
        if app.obstacleID == 1:
            triangle = shapes.Triangle(app.width - 20, app.height * 0.75, 
                                    app.width - 10, app.height * 0.75 - 25,
                                    app.width, app.height * 0.75, "orange", 
                                    app.height * 0.75 - 30)
            app.obstacles.append(triangle)

    # Creating Square
        elif app.obstacleID == 2:
            squareHeight = app.squareHeightScale * 30
            square = shapes.Square(app.width - 30, app.ground[2] - squareHeight,
                            app.width, app.ground[2], "purple")
            app.obstacles.append(square)

    # Creating obstacles for reverse gravity mode
    elif app.mode == "reverseGravityMode":
        rectangleHeight = 3 * app.pitches[app.pitchIndex]
        rectangleWidth = 30
        # Check what was the previous rectangle
        rectangleID = random.randint(1, 2)
        # Create rectangle at the bottom
        if rectangleID == 1:
            rectangle = shapes.Rectangle(app.width - rectangleWidth / 2,
                                         app.ground[2] - rectangleHeight / 2,
                                         rectangleHeight, rectangleWidth)

        # Create Rectangle at the top
        elif rectangleID == 2:
            rectangle = shapes.Rectangle(app.width - rectangleWidth / 2,
                                         app.ceiling[2] + rectangleHeight / 2,
                                         rectangleHeight, rectangleWidth)

        app.obstacles.append(rectangle)

    # Creating a mountain for the zigZagMode
    elif app.mode == "zigZagMode":
        # Here, the math works this way:
        # We will get the height of the biggest possible mountain
        # This will be 0.75 of the height of app.height
        constantHeight = app.height * 0.75
        # Then we will use random.randint to randomly obtain a value to scale
        heightScale = random.randint(1, 5)
        # After which, we will randomly get the actual height of the initialized triangle
        height = 0.2 * heightScale * constantHeight

        # Here, we will compute the random generation of the mountain obstacles
        # We will alternate between placing the mountains on the ceiling or on the ground
        # If there is nothing at the start, we will by default, we will initialize it on the ground
        # Else: if we will check app.obstacles[-1] if its on the gorund or not

        # Spawning mountain on the ground
        if ((app.obstacles == []) or (app.obstacles[-1].y0 == 0)):
            mountain = shapes.Mountain(app.width, app.height, 
                                    app.width + height, app.height - height,
                                    app.width + 2 * height, app.height,
                                    "black", height)
            app.obstacles.append(mountain)

        # If the obstacles are on the ceiling
        elif (app.obstacles[-1].y0 == app.height):
            mountain = shapes.Mountain(app.width, 0, 
                                    app.width + height, 0 + height,
                                    app.width + 2 * height, 0,
                                    "grey", height)

            app.obstacles.append(mountain)

# Function to check if obstacles have been passed by magic square
# Must check the following conditions: 
# 1. That the x0 coordinate of the square is on the right of the obstacle

def passedObstacle(app, obstacle):
    # Passed Triangle
    if isinstance(obstacle, shapes.Triangle):
        if ((app.magicSquare.x0 > obstacle.x1)): return True

    # Passed Rectangle
    elif isinstance(obstacle, shapes.Square):
        if (app.magicSquare.x1 > obstacle.x0): return True

    elif isinstance(obstacle, shapes.Rectangle):
        if (app.magicSquare.x1 > obstacle.x0): return True

    # Passed Mountain
    elif isinstance(obstacle, shapes.Mountain):
        if ((app.magicSquare.x0 > obstacle.x2)): return True

    return False

# Function to remove obstacles once the obstacle goes out of range
def removeObstacle(app):
    for obstacle in app.obstacles:
        # Does not apply to portals
        if not (isinstance(obstacle, shapes.Portal) or isinstance(obstacle, shapes.Mountain)):
            if obstacle.x1 < 0:
                app.obstacles.remove(obstacle)

        elif isinstance(obstacle, shapes.Mountain):
            if obstacle.x2 < 0:
                app.obstacles.remove(obstacle) 
            

# Every x seconds, we move the entire map by one frame (all the obstacles)
def takeStep(app):
    # Just change move
    move = 5
    # Loop through obstacles
    for obstacle in app.obstacles:
        if isinstance(obstacle, shapes.Triangle):
            obstacle.x0 -= move
            obstacle.x1 -= move
            obstacle.x2 -= move

        elif isinstance(obstacle, shapes.Square):
            obstacle.x0 -= move
            obstacle.x1 -= move

        elif isinstance(obstacle, shapes.Portal):
            obstacle.cx -= move

        elif isinstance(obstacle, shapes.Rectangle):
            obstacle.x0 -= move
            obstacle.x1 -= move

        elif isinstance(obstacle, shapes.Mountain):
            obstacle.x0 -= move
            obstacle.x1 -= move
            obstacle.x2 -= move

# Must debug this!
def checkCollision(app):
    # Collision happens when x1 of the magicSquare > x0 of the obstacle
    # If the object has passed the obstacle, it is not counted
    for obstacle in app.obstacles:
        # If it is a triangle
        if isinstance(obstacle, shapes.Triangle):
            if ((app.magicSquare.x1 >= obstacle.x0) and 
                (obstacle.y1 <= app.magicSquare.y1 <= obstacle.y0) and 
                passedObstacle(app, obstacle) == False):
                app.gameMusic.stop()
                app.gameover = True
                app.mode = "gameOverMode"
                return True
        
        # If is a square
        elif isinstance(obstacle, shapes.Square):
            # If the magic square did not manage to make it past the square obstacle
            # If the magic square is on top of the square obstacle, it stays there.
            if (((obstacle.x0 <= app.magicSquare.x1 <= obstacle.x1) and
                  (obstacle.y0 - 3 <= app.magicSquare.y1 <= obstacle.y0 + 3)) or 
                  ((obstacle.x0 <= app.magicSquare.x0 <= obstacle.x1) and
                  (obstacle.y0 - 3 <= app.magicSquare.y1 <= obstacle.y0 + 3))):
                  # Change the variable:
                  app.isOnSquare = True
                  app.magicSquare.centerY = obstacle.y0 - (app.magicSquare.height / 2)
                  app.magicSquare.y1 = obstacle.y0
                  app.magicSquare.y0 = app.magicSquare.y1 - app.magicSquare.height
                  return False

            # If magic square is no longer on square
            elif (app.isOnSquare == True and 
                  app.magicSquare.x0 >= obstacle.x1):
                  app.isOnSquare = False

            # If there is a head on collision between square and magicSquare
            elif ((app.magicSquare.x1 >= obstacle.x0) and
                (obstacle.y0 <= app.magicSquare.y1 <= obstacle.y1) and
                passedObstacle(app, obstacle) == False):
                app.gameMusic.stop()
                app.gameover = True
                app.mode = "gameOverMode"
                return True

        # If collide with a portal, change to another gameMode 
        elif isinstance(obstacle, shapes.Portal):
            # Check if the center of the portal lies within the magicSquare
            portalLeftX = obstacle.cx - app.smallPortalImage.width / 2
            portalBottomY = obstacle.cy + app.smallPortalImage.height / 2
            portalRightX = obstacle.cx + app.smallPortalImage.width / 2
            portalTopY = obstacle.cy - app.smallPortalImage.height / 2
            if ((portalLeftX <= app.magicSquare.centerX <= portalRightX) and
                portalTopY <= app.magicSquare.centerY <= portalBottomY):
                app.isOnPortal = True
                # Select a random mode to change to
                mode = ""
                while True:
                    mode = random.choice(app.modesList)
                    # If the mode is the same, we will try until we get a different mode
                    if mode != app.mode:
                        break
                app.mode = mode
                # For debugging: 
                # app.mode = "reverseGravityMode"
                # Remove the portal
                if app.mode == "gameMode":
                    app.squareHeightScale = 1
                app.obstacles.pop()
                app.magicSquare.centerY = app.height * 0.75 - 15
                app.magicSquare.y1 = app.ground[2]
                app.magicSquare.y0 = app.ground[2] - app.magicSquare.height
                # Change background color
                app.backgroundColor = app.modesDict[app.mode]
                app.isOnPortal = False
            else:
                app.isOnPortal = False
        
        elif isinstance(obstacle, shapes.Rectangle):
            # Check if the rectangle collides with the magicSquare
            if ((app.magicSquare.x1 >= obstacle.x0) and
            (obstacle.y0 <= app.magicSquare.y1 <= obstacle.y1) and
            passedObstacle(app, obstacle) == False):
                app.gameMusic.stop()
                app.gameover = True
                app.mode = "gameOverMode"
                return True

        elif isinstance(obstacle, shapes.Mountain):
            # Doing the linear algebra to find intersection
            # Four cases: For each for corner collision
            # 1. Bottom right. 2. Top right. 3. Bottom Left. 4. Top left
            # 1. Finding the gradient. Gradient = (y1 - y0) / (x1 - x0)
            gradient1 = (obstacle.y1 - obstacle.y0) / (obstacle.x1 - obstacle.x0)
            gradient2 = (obstacle.y2 - obstacle.y1) / (obstacle.x2 - obstacle.x1)
            # Getting the linear equation
            y_first = gradient1 * (app.magicSquare.x1 - obstacle.x1) + obstacle.y1
            y_second = gradient2 * (app.magicSquare.x0 - obstacle.x1) + obstacle.y1
            # This is a bug
            # if ((obstacle.x0 <= app.magicSquare.x1 <= obstacle.x1) and
            #     ((app.magicSquare.y1 < y_first) or 
            #    ((app.magicSquare.y1 - app.magicSquare.height) <= y_second))):
            #     app.gameover = True
            #     app.mode = "gameOverMode"
            #     return True

    return False

# ------------------------------------------------------------------------------
##########################  SPLASH SCREEN MODE  ################################
# ------------------------------------------------------------------------------

# Creating random shape
def addShape(app):
    randomX = random.randint(0, app.width // 2)
    randomY = random.randint(0, app.height // 2)
    randomDirection = random.choice(directions)
    app.shapes.append([randomX, randomY, randomDirection])

# Creating a function to move shape
def moveShape(app):
    for shape in app.shapes:
        (drow, dcol) = shape[2]
        shape[0] += drow
        shape[1] += dcol

def splashScreenMode_redrawAll(app, canvas):
    # Draw the background
    canvas.create_image(app.width / 2, app.height / 2, 
                        image = ImageTk.PhotoImage(app.splashScreenBackground))

    # Draw through the list of squares
    for shape in app.shapes:
        colors = ["red", "green", "blue", "yellow", "pink"]
        randomColor = random.choice(colors)
        cx, cy = shape[0], shape[1]
        canvas.create_rectangle(cx - 20, cy - 20, 
                                cx + 20, cy + 20, 
                                fill = randomColor, width = 3)

    # Geometry dash logo
    canvas.create_image(app.width / 2, app.height / 2 - 100, 
                    image=ImageTk.PhotoImage(app.splashScreenLogo))


    # Play Button
    if app.playButtonBig == False:
        canvas.create_image(app.width / 2, app.height / 2 + 30, 
                image=ImageTk.PhotoImage(app.splashScreenPlaySmallButton))
    else:
        canvas.create_image(app.width / 2, app.height / 2 + 30, 
                image=ImageTk.PhotoImage(app.splashScreenPlayButton))


    # High Score
    if app.highScoreBig == False:
        canvas.create_image(app.width / 2 + 200, app.height / 2 + 30, 
                        image=ImageTk.PhotoImage(app.highScoreSmallImage))
    else:
        canvas.create_image(app.width / 2 + 200, app.height / 2 + 30, 
                image=ImageTk.PhotoImage(app.highScoreImage))

    # Map Packs
    if app.mapPackBig == False:
        canvas.create_image(app.width / 2 - 200, app.height / 2 + 30, 
                        image=ImageTk.PhotoImage(app.mapPackSmallImage))
    else:
        canvas.create_image(app.width / 2 - 200, app.height / 2 + 30, 
                        image=ImageTk.PhotoImage(app.mapPackImage))

def splashScreenMode_keyPressed(app, event):
    return

def splashScreenMode_mousePressed(app, event):
    # Mouse Pressed
    cx = event.x
    cy = event.y

    # If mouse pressed in the play button
    playButtonWidth, playButtonheight = app.splashScreenPlaySmallButton.size
    playButtonWidthLeft = app.width / 2 - playButtonWidth
    playButtonWidthRight = app.width / 2 + playButtonWidth
    playButtonHeightLeft = (app.height / 2 + 30) - playButtonheight
    playButtonHeightRight = (app.height / 2 + 30) + playButtonheight
    if ((playButtonWidthLeft <= cx <= playButtonWidthRight) and 
        (playButtonHeightLeft <= cy <= playButtonHeightRight)):
        app.mode = "gameMode"
        app.gameMusic = sound.Sound(app.filename)
        app.score = 0
        # Stop splash screen music
        app.splashScreenMusic.stop()
        # Only start the song when the music has ended
        app.gameMusic.start()

    # If mouse pressed in the high score button
    highScoreButtonWidth, highScoreButtonheight = app.highScoreSmallImage.size
    highScoreButtonWidthLeft = (app.width / 2 + 200) - highScoreButtonWidth
    highScoreButtonWidthRight = (app.width / 2 + 200) + highScoreButtonWidth
    highScoreButtonHeightLeft = (app.height / 2 + 30) - highScoreButtonheight
    highScoreButtonHeightRight = (app.height / 2 + 30) + highScoreButtonheight
    
    if ((highScoreButtonWidthLeft <= cx <= highScoreButtonWidthRight) and 
        (highScoreButtonHeightLeft <= cy <= highScoreButtonHeightRight)):
        app.mode = 'highScore'

    # If mouse pressed in the map pack button

    mapPackButtonWidth, mapPackButtonheight = app.mapPackSmallImage.size
    mapPackButtonWidthLeft = (app.width / 2 - 200) - mapPackButtonWidth
    mapPackButtonWidthRight = (app.width / 2 - 200) + mapPackButtonWidth
    mapPackButtonHeightLeft = (app.height / 2 + 30) - mapPackButtonheight
    mapPackButtonHeightRight = (app.height / 2 + 30) + mapPackButtonheight
    if ((mapPackButtonWidthLeft <= cx <= mapPackButtonWidthRight) and 
        (mapPackButtonHeightLeft <= cy <= mapPackButtonHeightRight)):
        app.mode = 'mapPack'

def splashScreenMode_mouseMoved(app, event):
    cx, cy = event.x, event.y
    # If mouse hovered in the play button
    playButtonWidth, playButtonheight = app.splashScreenPlaySmallButton.size
    playButtonWidthLeft = app.width / 2 - playButtonWidth
    playButtonWidthRight = app.width / 2 + playButtonWidth
    playButtonHeightLeft = (app.height / 2 + 30) - playButtonheight
    playButtonHeightRight = (app.height / 2 + 30) + playButtonheight

    if ((playButtonWidthLeft <= cx <= playButtonWidthRight) and 
    (playButtonHeightLeft <= cy <= playButtonHeightRight)):
        app.playButtonBig = True
    else:
        app.playButtonBig = False

    # If mouse hovered in mapPack:
    mapPackButtonWidth, mapPackButtonheight = app.mapPackSmallImage.size
    mapPackButtonWidthLeft = (app.width / 2 - 200) - mapPackButtonWidth
    mapPackButtonWidthRight = (app.width / 2 - 200) + mapPackButtonWidth
    mapPackButtonHeightLeft = (app.height / 2 + 30) - mapPackButtonheight
    mapPackButtonHeightRight = (app.height / 2 + 30) + mapPackButtonheight
    if ((mapPackButtonWidthLeft <= cx <= mapPackButtonWidthRight) and 
        (mapPackButtonHeightLeft <= cy <= mapPackButtonHeightRight)):
        app.mapPackBig = True
    else:
        app.mapPackBig = False

    # If mouse hovered in high scores
    highScoreButtonWidth, highScoreButtonheight = app.highScoreSmallImage.size
    highScoreButtonWidthLeft = (app.width / 2 + 200) - highScoreButtonWidth
    highScoreButtonWidthRight = (app.width / 2 + 200) + highScoreButtonWidth
    highScoreButtonHeightLeft = (app.height / 2 + 30) - highScoreButtonheight
    highScoreButtonHeightRight = (app.height / 2 + 30) + highScoreButtonheight
    
    if ((highScoreButtonWidthLeft <= cx <= highScoreButtonWidthRight) and 
        (highScoreButtonHeightLeft <= cy <= highScoreButtonHeightRight)):
        app.highScoreBig = True
    else:
        app.highScoreBig = False

def splashScreenMode_timerFired(app):
    # if app.timeElapsed / app.timeDelay == 10:
    #     addShape(app)
    # moveShape(app)
    #app.timeElapsed += app.timerDelay
    if app.gameMusic != None:
        app.gameMusic.stop()
    return
# ------------------------------------------------------------------------------
#################################  GAME MODE  ##################################
# ------------------------------------------------------------------------------

def gameMode_redrawAll(app, canvas):
    # Can create the image, but it is very slow
    drawBackground(app, canvas)
    drawGround(app, canvas)
    drawMagicSquare(app, canvas)
    drawObstacles(app, canvas)
    drawScore(app, canvas)
    drawPauseButton(app, canvas)

def gameMode_keyPressed(app, event):
    # Jumping
    if event.key == "Space":
        # Can only jump if the square is on the ground or on some object
        if app.isInAir == False or app.isOnSquare == True:
            app.magicSquare.jump()
            app.isInAir = True
            app.isOnSquare = False

def gameMode_mousePressed(app, event):
    cx = event.x
    cy = event.y
    pauseButtonWidthLeft = 30 - app.smallPauseButton.width
    pauseButtonWidthRight = 30 + app.smallPauseButton.width
    pauseButtonHeightLeft = 30 - app.smallPauseButton.height
    pauseButtonHeightRight = 30 + app.smallPauseButton.height
    if ((pauseButtonWidthLeft <= cx <= pauseButtonWidthRight) and 
        (pauseButtonHeightLeft <= cy <= pauseButtonHeightRight)):
        app.mode = 'pauseMode'

def gameMode_timerFired(app):
    # Start the time the moment game starts:
    if app.startTime == 0:
        app.startTime = time.time()
    if app.realStartTime == 0:
        app.realStartTime = time.time()
    
    # End the game if there is a collision
    if checkCollision(app) == True: return

    # Calculate the total time that has elapsed since previous obstacle
    newTime = time.time()

    # Temporary time passed variable for period calculation
    tempTimePassed = newTime - app.startTime
    app.tempTimePassed = newTime - app.startTimeOne
    # Actual time passed
    app.timeElapsed = newTime - app.realStartTime
    app.score = int(app.timeElapsed / app.duration * 100)
    # Adding 1 to the pitch index every time a period passes
    if tempTimePassed > app.period:
        if app.pitchIndex < len(app.pitches):
            app.pitchIndex += 1
        else:
            app.pitchIndex = 0
    
    # Adding the obstacles based on the frequency of pitches
    if 0 <= app.pitches[app.pitchIndex] < app.pitchOne:
        app.obstacleID = 1
        if tempTimePassed > app.period:
            if app.obstacles == []: 
                addObstacle(app)

            elif not isinstance(app.obstacles[-1], shapes.Portal):
                addObstacle(app)
            app.startTime = newTime


    # If the pitch is medium
    elif app.pitchOne <= app.pitches[app.pitchIndex] < app.pitchTwo:
        app.obstacleID = random.randint(1, 2)
        if app.obstacleID == 1:
            app.obstacleID = 2
        if tempTimePassed > app.period / 2:
            if app.obstacles == []: 
                addObstacle(app)

            elif not isinstance(app.obstacles[-1], shapes.Portal):
                addObstacle(app)
            app.startTime = newTime

    # If the pitch is high
    else:
        app.obstacleID = 2
        if app.obstacleID == 1:
            app.obstacleID = 2
        if tempTimePassed > app.period / 4:
            if app.obstacleID == 1:
                app.obstacleID = 2
            if app.obstacles == []:
                if app.squareHeightScale == 3:
                    # If reach the third one: One of the three options can occur
                    # 1. 3rd rectangle taller than second
                    # 2. Triangle
                    # 3. 3rd rectangle taller than second
                    app.squareHeightScale = random.randint(1, 3)
                    if app.obstacleID == 1:
                        app.obstacleID = 2
                    else:
                        app.obstacleID = random.randint(1, 2)
                addObstacle(app)

            elif not isinstance(app.obstacles[-1], shapes.Portal):
                if app.squareHeightScale == 3:
                    app.squareHeightScale = random.randint(1, 3)
                    if isinstance(app.obstacles[-1], shapes.Triangle):
                        app.obstacleID = 2
                    else:
                        app.obstacleID = random.randint(1, 2)
                addObstacle(app)

            # Change the height if it is a square
            if isinstance(app.obstacles[-1], shapes.Square):
                if app.scaleAscending == True:
                    app.squareHeightScale += 1
                    if app.squareHeightScale == 3:
                        app.scaleAscending = False

                else:
                    if app.squareHeightScale == 1:
                        app.scaleAscending = True
                    app.squareHeightScale -= 1
                
            app.startTime = newTime
    
    # Move the entire map based on timerFired
    takeStep(app)
    # Check if any obstacles should be removed from the list of obstacles.
    removeObstacle(app)

    # Periodic dropping of the square if the square is above the ground.
    # Only drop when not sitting on the square
    if app.ground[2] - 5 <= app.magicSquare.y1 <= app.ground[2] + 5:
        app.isInAir = False
        app.magicSquare.centerY = app.ground[2] - (app.magicSquare.height / 2)
        app.magicSquare.y1 = app.ground[2]
        app.magicSquare.y0 = app.magicSquare.y1 - app.magicSquare.height

    # Drop when no longer sitting on the square
    if app.isInAir == True and app.isOnSquare == False:
        if app.magicSquare.y1 != app.ground[2]:
            app.magicSquare.drop()

    # "Acceleration"
    if (app.magicSquare.velocity != 10):
        app.magicSquare.velocity += 2

    # Changing the background color as time goes by
    changeBackgroundColorGradually(app)

    # Stop the game if it reaches 100%
    if app.score == 100 and app.isOnPortal == True:
        app.mode = "endMode"
        app.gameMusic.stop()

# ------------------------------------------------------------------------------
#########################          ZIGZAG MODE        ##########################
# ------------------------------------------------------------------------------

def zigZagMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawMagicSquare(app, canvas)
    drawObstacles(app, canvas)
    drawScore(app, canvas)
    drawPauseButton(app, canvas)

def zigZagMode_keyPressed(app, event):
    # Perform the Zig Zags!
    if event.key == "Space":
        if app.isDropping == True:
            app.isDropping = False

        elif app.isDropping == False:
            app.isDropping = True

def zigZagMode_mousePressed(app, event):
    cx = event.x
    cy = event.y
    pauseButtonWidthLeft = 30 - app.smallPauseButton.width
    pauseButtonWidthRight = 30 + app.smallPauseButton.width
    pauseButtonHeightLeft = 30 - app.smallPauseButton.height
    pauseButtonHeightRight = 30 + app.smallPauseButton.height
    if ((pauseButtonWidthLeft <= cx <= pauseButtonWidthRight) and 
        (pauseButtonHeightLeft <= cy <= pauseButtonHeightRight)):
        app.mode = 'pauseMode'

def zigZagMode_timerFired(app):
    # Start the time the moment game starts:
    if app.startTime == 0:
        app.startTime = time.time()
    if app.realStartTime == 0:
        app.realStartTime = time.time()
    
    # End the game if there is a collision
    if checkCollision(app) == True: return

    # Calculate the total time that has elapsed since previous obstacle
    newTime = time.time()

    # Temporary time passed variable for period calculation
    tempTimePassed = newTime - app.startTime
    if app.tempTimePassed > app.period:
        if app.pitchIndex < len(app.pitches):
            app.pitchIndex += 1
        else:
            app.pitchIndex = 0
        app.startTimeOne = newTime
    # Actual time passed
    app.timeElapsed = newTime - app.realStartTime
    app.score = int(app.timeElapsed / app.duration * 100)

    if (app.obstacles != []) and isinstance(app.obstacles[-1], shapes.Portal):
        pass
    elif (app.obstacles == []) or (app.obstacles[-1].x1 == app.width):
        # So no mountains are generated near the portal
        #if app.score % 10 < 8 or app.score % 10 == 0:
        addObstacle(app)
    
    # Move the entire map based on timerFired
    takeStep(app)
    # Check if any obstacles should be removed from the list of obstacles.
    removeObstacle(app)

    # While loop to perform the zigZag
    if app.isDropping == True and app.magicSquare.y1 != app.height:
        app.magicSquare.fastDrop()

    elif app.isDropping == False and app.magicSquare.y0 != 0:
        app.magicSquare.fly()

    # Changing the background color as time goes by
    changeBackgroundColorGradually(app)

    # Stop the game if it reaches 100%
    if app.score == 100 and app.isOnPortal == True:
        app.mode = "endMode"
        app.gameMusic.stop()

# ------------------------------------------------------------------------------
#####################          REVERSE GRAVITY MODE        #####################
# ------------------------------------------------------------------------------

def reverseGravityMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawGround(app, canvas)
    drawCeiling(app, canvas)
    drawMagicSquare(app, canvas)
    drawObstacles(app, canvas)
    drawScore(app, canvas)
    drawPauseButton(app, canvas)

def reverseGravityMode_keyPressed(app, event):
    if event.key == "Space":
        # Can only jump if the square is on the ground or on some object
        app.magicSquare.teleport(app.ground, app.ceiling)

def reverseGravityMode_mousePressed(app, event):
    cx = event.x
    cy = event.y
    pauseButtonWidthLeft = 30 - app.smallPauseButton.width
    pauseButtonWidthRight = 30 + app.smallPauseButton.width
    pauseButtonHeightLeft = 30 - app.smallPauseButton.height
    pauseButtonHeightRight = 30 + app.smallPauseButton.height
    if ((pauseButtonWidthLeft <= cx <= pauseButtonWidthRight) and 
        (pauseButtonHeightLeft <= cy <= pauseButtonHeightRight)):
        app.mode = 'pauseMode'

def reverseGravityMode_timerFired(app):
    # Start the time the moment game starts:
    if app.startTime == 0:
        app.startTime = time.time()
    if app.realStartTime == 0:
        app.realStartTime = time.time()
    
    # End the game if there is a collision
    if checkCollision(app) == True: return

    # Calculate the total time that has elapsed since previous obstacle
    newTime = time.time()

    # Temporary time passed variable for period calculation
    tempTimePassed = newTime - app.startTime
    # Actual time passed
    app.timeElapsed = newTime - app.realStartTime
    app.score = int(app.timeElapsed / app.duration * 100)
    # Adding 1 to the pitch index every time a period passes
    app.tempTimePassed = newTime - app.startTimeOne
    if app.tempTimePassed > app.period:
        if app.pitchIndex < len(app.pitches):
            app.pitchIndex += 1
        else:
            app.pitchIndex = 0
        app.startTimeOne = newTime
    
    # Adding the obstacles based on the frequency of pitches
    if 0 <= app.pitches[app.pitchIndex] < app.pitchOne:
        if tempTimePassed > app.period / 2:
            if app.obstacles == []: 
                addObstacle(app)

            elif not isinstance(app.obstacles[-1], shapes.Portal):
                addObstacle(app)
            app.startTime = newTime

    # If the pitch is medium
    elif app.pitchOne <= app.pitches[app.pitchIndex] < app.pitchOne:
        if tempTimePassed > app.period / 2:
            if app.obstacles == []: 
                addObstacle(app)

            elif not isinstance(app.obstacles[-1], shapes.Portal):
                addObstacle(app)
            app.startTime = newTime

    # If the pitch is high
    else:
        if tempTimePassed > app.period / 2:
            if app.obstacles == []: 
                addObstacle(app)

            elif not isinstance(app.obstacles[-1], shapes.Portal):
                addObstacle(app)

            app.startTime = newTime
    
    # Move the entire map based on timerFired
    takeStep(app)
    # Check if any obstacles should be removed from the list of obstacles.
    removeObstacle(app)

    # Periodic dropping of the square if the square is above the ground.
    # Only drop when not sitting on the square
    if app.magicSquare.y1 == app.ground[2]:
        app.isInAir = False

    # Drop when no longer sitting on the square
    if app.isInAir == True and app.isOnSquare == False:
        if app.magicSquare.y1 != app.ground[2]:
            app.magicSquare.drop()

    # Changing the background color as time goes by
    changeBackgroundColorGradually(app)

    # Stop the game if it reaches 100%
    if app.score == 100 and app.isOnPortal == True:
        app.mode = "endMode"
        app.gameMusic.stop()
        

# ------------------------------------------------------------------------------
########################         HIGH SCORE MODE       #########################
# ------------------------------------------------------------------------------

def drawBackButton(app, canvas):
    if app.backButtonBig == False:
        canvas.create_image(30, 30,
                        image = ImageTk.PhotoImage(app.backSmallButton))
    else:
        canvas.create_image(30, 30,
                        image = ImageTk.PhotoImage(app.backButton))  

def drawPauseButton(app, canvas):
    canvas.create_image(30, 30,
                        image = ImageTk.PhotoImage(app.smallPauseButton))

def highScore_redrawAll(app, canvas):
    # Draw the background
    canvas.create_image(app.width / 2, app.height / 2, 
                        image = ImageTk.PhotoImage(app.splashScreenBackground))

    # Create the button
    drawBackButton(app, canvas)

def highScore_keyPressed(app, event):
    return

def highScore_mousePressed(app, event):
    cx = event.x
    cy = event.y
    backButtonWidthLeft = 30 - app.backSmallButton.width
    backButtonWidthRight = 30 + app.backSmallButton.width
    backButtonHeightLeft = 30 - app.backSmallButton.height
    backButtonHeightRight = 30 + app.backSmallButton.height
    if ((backButtonWidthLeft <= cx <= backButtonWidthRight) and 
        (backButtonHeightLeft <= cy <= backButtonHeightRight)):
        app.mode = 'splashScreenMode'

def highScore_mouseMoved(app, event):
    cx, cy = event.x, event.y
    backButtonWidthLeft = 30 - app.backSmallButton.width
    backButtonWidthRight = 30 + app.backSmallButton.width
    backButtonHeightLeft = 30 - app.backSmallButton.height
    backButtonHeightRight = 30 + app.backSmallButton.height
    if ((backButtonWidthLeft <= cx <= backButtonWidthRight) and 
        (backButtonHeightLeft <= cy <= backButtonHeightRight)):
        app.backButtonBig == True
    else:
        app.backButtonBig == False


def highScore_timerFired(app):
    return
        

# ------------------------------------------------------------------------------
########################          MAP PACK MODE        #########################
# ------------------------------------------------------------------------------

def mapPack_redrawAll(app, canvas):
    # Draw the background
    canvas.create_image(app.width / 2, app.height / 2, 
                        image = ImageTk.PhotoImage(app.splashScreenBackground))

    # Create the button
    canvas.create_image(30, 30, 
                        image = ImageTk.PhotoImage(app.backSmallButton))

    # Create the prompt
    canvas.create_text(app.width / 2, app.height / 2 - 100, 
                       text = "File path of your song: ", 
                       font = "Arial 26 bold")
    # Drawing input box
    canvas.create_rectangle(50, app.height / 2 - 80, app.width - 50, 
                            app.height / 2 - 40, fill = "white", width = 3)

    # Drawing the input
    canvas.create_text(app.width / 2, app.height / 2 - 60, 
                            text = f"{app.filename}", font = "Arial 23 bold")

    # Prompt for the song name
    canvas.create_text(app.width / 2, app.height / 2, 
                       text = "Song name: ", 
                       font = "Arial 26 bold")

    # Drawing another input box
    canvas.create_rectangle(100, app.height / 2 + 20, app.width - 100, 
                            app.height / 2 + 60, fill = "white", width = 3)

def mapPack_keyPressed(app, event):
    return

def mapPack_mousePressed(app, event):
    cx = event.x
    cy = event.y
    # If pressed the back button
    backButtonWidthLeft = 30 - app.backSmallButton.width
    backButtonWidthRight = 30 + app.backSmallButton.width
    backButtonHeightLeft = 30 - app.backSmallButton.height
    backButtonHeightRight = 30 + app.backSmallButton.height
    if ((backButtonWidthLeft <= cx <= backButtonWidthRight) and 
        (backButtonHeightLeft <= cy <= backButtonHeightRight)):
        app.mode = 'splashScreenMode'

    # If pressed inside the box
    box1WidthLeft = 50
    box1WidthRight = app.width - 50
    box1HeightLeft = app.height / 2 - 80
    box1HeightRight = app.height / 2 - 40
    if ((box1WidthLeft <= cx <= box1WidthRight) and 
        (box1HeightLeft <= cy <= box1HeightRight)):
        app.filename = app.getUserInput("File path of song: ")

def mapPack_mouseMoved(app, event):
    cx, cy = event.x, event.y
    backButtonWidthLeft = 30 - app.backSmallButton.width
    backButtonWidthRight = 30 + app.backSmallButton.width
    backButtonHeightLeft = 30 - app.backSmallButton.height
    backButtonHeightRight = 30 + app.backSmallButton.height
    if ((backButtonWidthLeft <= cx <= backButtonWidthRight) and 
        (backButtonHeightLeft <= cy <= backButtonHeightRight)):
        app.backButtonBig == True
    else:
        app.backButtonBig == False

def mapPack_timerFired(app):
    return

# ------------------------------------------------------------------------------
##############################  GAME OVER MODE  ################################
# ------------------------------------------------------------------------------

def drawFinalScore(app, canvas):
    canvas.create_text(app.width / 2, app.height / 2 - 100, 
                       text = f"Score: {app.score}%", font = "Arial 30 bold",
                       fill = "white")

def gameOverMode_redrawAll(app, canvas):
    # Black background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")

    # Game Over Image
    canvas.create_image(app.width / 2, app.height / 2 - 135,
                        image = ImageTk.PhotoImage(app.smallGameOverImage))

    # Draw score
    drawFinalScore(app, canvas)

    # Replay button to restart the game
    if app.replayButtonBig == False:
        canvas.create_image(app.width / 2, app.height / 2,
                        image = ImageTk.PhotoImage(app.smallReplayButton))
    else:
        canvas.create_image(app.width / 2, app.height / 2,
                        image = ImageTk.PhotoImage(app.mediumReplayButton))
                        
    # Return to home button
    if app.returnHomeBig == False:
        canvas.create_image(app.width / 2, app.height / 2 + 120, 
                        image = ImageTk.PhotoImage(app.smallHomeButton))
    else:
        canvas.create_image(app.width / 2, app.height / 2 + 120, 
                        image = ImageTk.PhotoImage(app.mediumHomeButton))

    #TODO: Make this better
    # Words in return to home button
    if app.returnHomeBig == False:
        canvas.create_text(app.width / 2, app.height / 2 + 120, 
                           text = "Return to home", font = "Arial 18 bold")
    else:
        canvas.create_text(app.width / 2, app.height / 2 + 120, 
                           text = "Return to home", font = "Arial 26 bold")

def gameOverMode_keyPressed(app, event):
    return

def gameOverMode_mousePressed(app, event):
    # Location of mousePressed
    cx = event.x
    cy = event.y

    # Mouse pressed within replay button, go back to gameMode
    # TODO: There is a bug, the game needs to restart during gameMode.

    replayButtonWidthLeft = app.width / 2 - app.smallReplayButton.width
    replayButtonWidthRight = app.width / 2 + app.smallReplayButton.width
    replayButtonHeightLeft = app.height / 2 - app.smallReplayButton.height
    replayButtonHeightRight = app.height / 2 + app.smallReplayButton.height
    if ((replayButtonWidthLeft <= cx <= replayButtonWidthRight) and 
        (replayButtonHeightLeft <= cy <= replayButtonHeightRight)):
        app.mode = 'gameMode'
        restartGame(app)
        app.gameMusic = sound.Sound(app.filename)
        app.gameMusic.start()
    
    # Mouse pressed in return to home button, go back to splash screen
    homeButtonWidthLeft = app.width / 2 - app.smallHomeButton.width
    homeButtonWidthRight = app.width / 2 + app.smallHomeButton.width
    homeButtonHeightLeft = (app.height / 2 + 120) - app.smallHomeButton.height
    homeButtonHeightRight = (app.height / 2 + 120) + app.smallHomeButton.height
    if ((homeButtonWidthLeft <= cx <= homeButtonWidthRight) and 
        (homeButtonHeightLeft <= cy <= homeButtonHeightRight)):
        app.gameMusic.stop()
        app.mode = 'splashScreenMode'
        app.splashScreenMusic.start()

def gameOverMode_mouseMoved(app, event):
    cx, cy = event.x, event.y
    # Replay button
    replayButtonWidthLeft = app.width / 2 - app.smallReplayButton.width
    replayButtonWidthRight = app.width / 2 + app.smallReplayButton.width
    replayButtonHeightLeft = app.height / 2 - app.smallReplayButton.height
    replayButtonHeightRight = app.height / 2 + app.smallReplayButton.height
    if ((replayButtonWidthLeft <= cx <= replayButtonWidthRight) and 
        (replayButtonHeightLeft <= cy <= replayButtonHeightRight)):
        app.replayButtonBig = True
    else:
        app.replayButtonBig = False

    # Home Button
    homeButtonWidthLeft = app.width / 2 - app.smallHomeButton.width
    homeButtonWidthRight = app.width / 2 + app.smallHomeButton.width
    homeButtonHeightLeft = (app.height / 2 + 120) - app.smallHomeButton.height
    homeButtonHeightRight = (app.height / 2 + 120) + app.smallHomeButton.height
    if ((homeButtonWidthLeft <= cx <= homeButtonWidthRight) and 
        (homeButtonHeightLeft <= cy <= homeButtonHeightRight)):
        app.returnHomeBig = True
    else:
        app.returnHomeBig = False

def gameOverMode_timerFired(app):
    return

# ------------------------------------------------------------------------------
#################################  PAUSE MODE  #################################
# ------------------------------------------------------------------------------

def pauseMode_redrawAll(app, canvas):
    # Black background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")

    # Pause Image
    canvas.create_image(app.width / 2, app.height / 2 - 150,
                        image = ImageTk.PhotoImage(app.smallPausedImage))

    # Draw score
    drawFinalScore(app, canvas)

    # Replay button to restart the game
    if app.replayButtonBig == False:
        canvas.create_image(app.width / 2, app.height / 2,
                        image = ImageTk.PhotoImage(app.smallReplayButton))
    else:
        canvas.create_image(app.width / 2, app.height / 2,
                        image = ImageTk.PhotoImage(app.mediumReplayButton))
                        
    # Return to home button
    if app.returnHomeBig == False:
        canvas.create_image(app.width / 2, app.height / 2 + 120, 
                        image = ImageTk.PhotoImage(app.smallHomeButton))
    else:
        canvas.create_image(app.width / 2, app.height / 2 + 120, 
                        image = ImageTk.PhotoImage(app.mediumHomeButton))

    #TODO: Make this better
    # Words in return to home button
    if app.returnHomeBig == False:
        canvas.create_text(app.width / 2, app.height / 2 + 120, 
                           text = "Return to home", font = "Arial 18 bold")
    else:
        canvas.create_text(app.width / 2, app.height / 2 + 120, 
                           text = "Return to home", font = "Arial 26 bold")

def pauseMode_keyPressed(app, event):
    return

def pauseMode_mousePressed(app, event):
    # Location of mousePressed
    cx = event.x
    cy = event.y

    # Mouse pressed within replay button, go back to gameMode
    # TODO: There is a bug, the game needs to restart during gameMode.

    replayButtonWidthLeft = app.width / 2 - app.smallReplayButton.width
    replayButtonWidthRight = app.width / 2 + app.smallReplayButton.width
    replayButtonHeightLeft = app.height / 2 - app.smallReplayButton.height
    replayButtonHeightRight = app.height / 2 + app.smallReplayButton.height
    if ((replayButtonWidthLeft <= cx <= replayButtonWidthRight) and 
        (replayButtonHeightLeft <= cy <= replayButtonHeightRight)):
        app.mode = 'gameMode'
        app.gameMusic.start()
    
    # Mouse pressed in return to home button, go back to splash screen
    homeButtonWidthLeft = app.width / 2 - app.smallHomeButton.width
    homeButtonWidthRight = app.width / 2 + app.smallHomeButton.width
    homeButtonHeightLeft = (app.height / 2 + 120) - app.smallHomeButton.height
    homeButtonHeightRight = (app.height / 2 + 120) + app.smallHomeButton.height
    if ((homeButtonWidthLeft <= cx <= homeButtonWidthRight) and 
        (homeButtonHeightLeft <= cy <= homeButtonHeightRight)):
        app.gameMusic.stop()
        app.mode = 'splashScreenMode'
        app.splashScreenMusic.start()

def pauseMode_mouseMoved(app, event):
    cx, cy = event.x, event.y
    # Replay button
    replayButtonWidthLeft = app.width / 2 - app.smallReplayButton.width
    replayButtonWidthRight = app.width / 2 + app.smallReplayButton.width
    replayButtonHeightLeft = app.height / 2 - app.smallReplayButton.height
    replayButtonHeightRight = app.height / 2 + app.smallReplayButton.height
    if ((replayButtonWidthLeft <= cx <= replayButtonWidthRight) and 
        (replayButtonHeightLeft <= cy <= replayButtonHeightRight)):
        app.replayButtonBig = True
    else:
        app.replayButtonBig = False

    # Home Button
    homeButtonWidthLeft = app.width / 2 - app.smallHomeButton.width
    homeButtonWidthRight = app.width / 2 + app.smallHomeButton.width
    homeButtonHeightLeft = (app.height / 2 + 120) - app.smallHomeButton.height
    homeButtonHeightRight = (app.height / 2 + 120) + app.smallHomeButton.height
    if ((homeButtonWidthLeft <= cx <= homeButtonWidthRight) and 
        (homeButtonHeightLeft <= cy <= homeButtonHeightRight)):
        app.returnHomeBig = True
    else:
        app.returnHomeBig = False

def pauseMode_timerFired(app):
    return

# ------------------------------------------------------------------------------
##################################  END MODE  #################################
# ------------------------------------------------------------------------------

def endMode_redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, 
                        image = ImageTk.PhotoImage(app.smallCongratsImage))

def endMode_mousePressed(app, event):
    return

def endMode_timerFired(app):
    return

# ------------------------------------------------------------------------------
######################         RUNNING THE CODE        #########################
# ------------------------------------------------------------------------------

def playGeometryDash():
    runApp(width = 700, height = 400)

playGeometryDash()