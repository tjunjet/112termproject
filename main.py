# Importing the standard Python Libraries
from cmu_112_graphics import *
import random
import math
import os
import time
import pygame

# ------------------------------------------------------------------------------
#                           IMPORTING MY OWN LIBRARIES
# ------------------------------------------------------------------------------

import shapes
import bpm_detection
import sound
import pitch_detection

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
    app.label = 'Geometry Dash!'
    app.height = 400
    app.width = 700
    app.ground = (0, app.width, app.height * 0.75, app.height * 0.75)
    app.magicSquare = shapes.magicSquare(30, 30, "green", 
                       app.width / 5 + 10 , app.height * 0.75 - 15)
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

    # Adding additional parameters that we have configured
    soundOptions(app)
    timerOptions(app)
    graphicOptions(app)
    imageOptions(app)
    obstacleOptions(app)

# Drawing imageOptions
def imageOptions(app):
    # Creating images for the splash screen
    app.splashScreenBackground = app.loadImage("Images/geometry_dash_background.jpeg")
    app.splashScreenLogo = app.loadImage("Images/geometry-dash-logo.png")
    app.splashScreenPlayButton = app.loadImage("Images/geometry_dash_play_button.png")
    app.splashScreenPlaySmallButton = app.scaleImage(app.splashScreenPlayButton, 2/3)
    # High Scores and scaled
    app.highScoreImage = app.loadImage("Images/high_scores.png")
    app.highScoreSmallImage = app.scaleImage(app.highScoreImage, 1/2)
    # Map pack image and scaled
    app.mapPackImage = app.loadImage("Images/map_packs.png")
    app.mapPackSmallImage = app.scaleImage(app.mapPackImage, 1/2)
    # Back button
    app.backButton = app.loadImage("Images/back_button.png")
    app.backSmallButton = app.scaleImage(app.backButton, 0.1)
    # Game over image
    app.gameOverImage = app.loadImage("Images/game_over.png")
    app.smallGameOverImage = app.scaleImage(app.gameOverImage, 0.1)
    # Replay button image
    app.replayButton = app.loadImage("Images/replay_button.png")
    app.smallReplayButton = app.scaleImage(app.replayButton, 0.5)
    # Return to home button
    app.returnToHomeButton = app.loadImage("Images/homeButton.png")
    app.smallHomeButton = app.scaleImage(app.returnToHomeButton, 0.4)

def obstacleOptions(app):
    return

# Graphics parameters
def graphicOptions(app):
    # Using a cool background image
    app.image1 = app.loadImage('background-min.jpeg')
    app.image2 = app.scaleImage(app.image1, 2/3)

    # Creating the shapes for the splash mode
    app.splashShapeList = []

    # Generating background color
    app.backgroundColor = [0, 0, 255]
    app.isIncreasing = True

# Function that contains all the sound parameters
def soundOptions(app):
    pygame.mixer.init()
    # Getting the filename of splash screen music
    app.splashScreenMusicFile = "Music/Geometry Dash OST _ Title Screen (Menu Loop).wav"
    # Getting the filename of the game song
    app.filename = "Music/Forever Bound - Stereo Madness.wav"
    # Gets the beat per minute of the song
    app.bpm = bpm_detection.get_bpm(app.filename)
    # Creating splash screen music
    app.splashScreenMusic = sound.Sound(app.splashScreenMusicFile)
    app.splashScreenMusic.start()
    # Getting the parameters to play song when the game starts
    app.gameMusic = sound.Sound(app.filename)
    # Period let's us know the time interval in which obstacles appear
    # Using the physics equation f = 1 / T
    # Frequency is the number of beats per minute (By definition of frequency)
    # Period: Defined as the time interval between successive beats
    # For now, I multiply 4 to period for simplicity
    app.period = 4 * 60 / app.bpm
    # Getting the list of pitches in the music
    app.pitches = pitch_detection.get_pitch(app.filename)

# Function that contains anything related to timerFired
def timerOptions(app):
    app.timerDelay = 20
    app.timeElapsed = 0
    # Getting the startTime so it is easier to compute BPM
    app.startTime = time.time()

# ------------------------------------------------------------------------------
#                               PROCESSING MUSIC
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#                            VIEW: DRAWING FUNCTIONS
# ------------------------------------------------------------------------------

# Getting random color
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

# Changing the background color gradually
def changeBackgroundColorGradually(app):
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
# Drawing the ground. This does not change throughout the game for now.

def drawGround(app, canvas):
    x0, x1, y0, y1 = app.ground
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

        # If it is a square, we draw a rectangle
        elif isinstance(obstacle, shapes.Square):
            drawSquare(app, canvas, 
                       obstacle.x0, obstacle.y0,
                       obstacle.x1, obstacle.y1, "purple")

        # If it is a portal, we draw circle
        elif isinstance(obstacle, shapes.Portal):
            return 


# ------------------------------------------------------------------------------
#                              CONTROLLER FUNCTIONS
# ------------------------------------------------------------------------------

# Function to add obstacles randomly based on the BPM

def addObstacle(app):
    obstacleID = random.randint(1, 2)
    # Create obstacle if obstacleID == 1
    if obstacleID == 1:
        triangle = shapes.Triangle(app.width - 20, app.height * 0.75, 
                                   app.width - 10, app.height * 0.75 - 25,
                                   app.width, app.height * 0.75, "orange", 
                                   app.height * 0.75 - 30)
        app.obstacles.append(triangle)

    elif obstacleID == 2:
        square = shapes.Square(app.width - 30, app.height * 0.75 - 30,
                        app.width, app.height * 0.75, "purple")
        app.obstacles.append(square)

# Function to check if obstacles have been passed by magic square
# Must check the following conditions: 
# 1. That the x0 coordinate of the square is on the right of the obstacle
# 2. 

def passedObstacle(app, obstacle):
    # Passed Triangle
    if isinstance(obstacle, shapes.Triangle):
        if ((app.magicSquare.x0 > obstacle.x1)): return True

    # Passed Rectangle
    elif isinstance(obstacle, shapes.Square):
        if (app.magicSquare.x1 > obstacle.x0): return True

    return False

# Function to remove obstacles once the obstacle goes out of range
def removeObstacle(app):
    for obstacle in app.obstacles:
        if obstacle.x1 < 0:
            app.obstacles.remove(obstacle)
        

# Every x seconds, we move the entire map by one frame (all the obstacles)
def takeStep(app):
    for obstacle in app.obstacles:
        if isinstance(obstacle, shapes.Triangle):
            obstacle.x0 -= 5
            obstacle.x1 -= 5
            obstacle.x2 -= 5

        elif isinstance(obstacle, shapes.Square):
            obstacle.x0 -= 5
            obstacle.x1 -= 5

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
                app.gameover = True
                app.mode = "gameOverMode"
                return True
        
        # If is a square
        elif isinstance(obstacle, shapes.Square):
            # If the magic square did not manage to make it past the square obstacle

            # If the magic square is on top of the square obstacle, it stays there.
            if ((obstacle.x0 <= app.magicSquare.x1 <= obstacle.x1) and
                  (app.magicSquare.y1 == obstacle.y0)):
                  # Change the variable:
                  app.isOnSquare = True
                  return False

            # If magic square is no longer on square
            elif (app.isOnSquare == True and 
                  app.magicSquare.x0 >= obstacle.x1):
                  return
            # If there is a head on collision between square and magicSquare
            elif ((app.magicSquare.x1 > obstacle.x0) and
                (app.magicSquare.y1 > obstacle.y0) and
                passedObstacle(app, obstacle) == False):
                app.gameover = True
                app.mode = "gameOverMode"
                return True

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
    canvas.create_image(app.width / 2, app.height / 2 + 30, 
                        image=ImageTk.PhotoImage(app.splashScreenPlaySmallButton))

    # High Score
    canvas.create_image(app.width / 2 + 200, app.height / 2 + 30, 
                        image=ImageTk.PhotoImage(app.highScoreSmallImage))

    # Map Packs
    canvas.create_image(app.width / 2 - 200, app.height / 2 + 30, 
                        image=ImageTk.PhotoImage(app.mapPackSmallImage))


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
        app.mode = 'gameMode'
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

def splashScreenMode_timerFired(app):
    # if app.timeElapsed / app.timeDelay == 10:
    #     addShape(app)
    # moveShape(app)
    app.timeElapsed += app.timerDelay
# ------------------------------------------------------------------------------
#################################  GAME MODE  ##################################
# ------------------------------------------------------------------------------

def gameMode_redrawAll(app, canvas):
    # Can create the image, but it is very slow
    #canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image2))
    drawBackground(app, canvas)
    drawGround(app, canvas)
    drawMagicSquare(app, canvas)
    drawObstacles(app, canvas)

def gameMode_keyPressed(app, event):
    # Jumping
    if event.key == "Space":
        # Can only jump if the square is on the ground or on some object
        if app.isInAir == False or app.isOnSquare == True:
            app.magicSquare.jump()
            app.isInAir = True
            app.isOnSquare = False

def gameMode_mousePressed(app, event):
    return 

def gameMode_timerFired(app):
    # End the game if there is a collision
    if checkCollision(app) == True: return
    # Calculate the total time that has elapsed since previous obstacle
    newTime = time.time()
    timePassed = newTime - app.startTime
    if timePassed > app.period:
        addObstacle(app)
        app.startTime = newTime
    
    # Move the entire map based on timerFired
    takeStep(app)
    # Check if any obstacles should be removed from the list of obstacles.
    removeObstacle(app)

    # Periodic dropping of the square if the square is above the ground.
    # Only drop when not sitting on the square
    if app.isOnSquare == False:
        if app.isInAir == True:
            app.magicSquare.drop()

    if app.magicSquare.y1 == app.ground[2]:
        app.isInAir = False

    #Checking if the magicSquare is on the square
    if app.isOnSquare == True:
        app.isInAir = True
        app.magicSquare.centerY = app.height * 0.75 + 15

    # Changing the background color as time goes by
    changeBackgroundColorGradually(app)


# ------------------------------------------------------------------------------
########################         HIGH SCORE MODE       #########################
# ------------------------------------------------------------------------------

def drawBackButton(app, canvas):
    canvas.create_image(30, 30,
                        image = ImageTk.PhotoImage(app.backSmallButton))

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

def mapPack_keyPressed(app, event):
    return

def mapPack_mousePressed(app, event):
    cx = event.x
    cy = event.y
    backButtonWidthLeft = 30 - app.backSmallButton.width
    backButtonWidthRight = 30 + app.backSmallButton.width
    backButtonHeightLeft = 30 - app.backSmallButton.height
    backButtonHeightRight = 30 + app.backSmallButton.height
    if ((backButtonWidthLeft <= cx <= backButtonWidthRight) and 
        (backButtonHeightLeft <= cy <= backButtonHeightRight)):
        app.mode = 'splashScreenMode'

def mapPack_timerFired(app):
    return

# ------------------------------------------------------------------------------
##############################  GAME OVER MODE  ################################
# ------------------------------------------------------------------------------

def gameOverMode_redrawAll(app, canvas):
    # Black background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    # Game Over Image
    canvas.create_image(app.width / 2, app.height / 2 - 100,
                        image = ImageTk.PhotoImage(app.smallGameOverImage))
    # Replay button to restart the game
    canvas.create_image(app.width / 2, app.height / 2,
                        image = ImageTk.PhotoImage(app.smallReplayButton))
    # Return to home button
    canvas.create_image(app.width / 2, app.height / 2 + 120, 
                        image = ImageTk.PhotoImage(app.smallHomeButton))

    #TODO: Make this better
    # Words in return to home button
    canvas.create_text(app.width / 2, app.height / 2 + 120, text = "Return to home")

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
        appStarted(app)
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

def gameOverMode_timerFired(app):
    return

# ------------------------------------------------------------------------------
#################################  PAUSE MODE  #################################
# ------------------------------------------------------------------------------

def pauseMode_redrawAll(app, canvas):
    # Drawing the pause button
    return

def pauseMode_keyPressed(app, event):
    return

def pauseMode_mousePressed(app, event):
    return

def pauseMode_timerFired(app):
    return

# ------------------------------------------------------------------------------
######################         RUNNING THE CODE        #########################
# ------------------------------------------------------------------------------

def playGeometryDash():
    runApp(width = 700, height = 400)

playGeometryDash()