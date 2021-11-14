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
    app.typesOfObstacles = []

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

    # Adding additional parameters that we have configured
    soundOptions(app)
    timerOptions(app)
    graphicOptions(app)
    imageOptions(app)

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

# Graphics parameters
def graphicOptions(app):
    # Using a cool background image
    app.image1 = app.loadImage('background-min.jpeg')
    app.image2 = app.scaleImage(app.image1, 2/3)

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
def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "blue")

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
            return

        # If it is a portal, we draw circle
        elif isinstance(obstacle, shapes.Portal):
            return 

# Drawing the game over sign
def drawGameOver(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "red")
    canvas.create_text(app.width / 2, app.height / 2, text="Game Over!",
                       fill="black", font="Helvetica 26 bold underline")


# ------------------------------------------------------------------------------
#                              CONTROLLER FUNCTIONS
# ------------------------------------------------------------------------------

# Function to add obstacles randomly based on the BPM

def addObstacle(app):
    #obstacleID = random.randint(1, 2)
    obstacleID = 1
    # Create obstacle if obstacleID == 1
    if obstacleID == 1:
        triangle = shapes.Triangle(app.width - 20, app.height * 0.75, 
                                   app.width - 10, app.height * 0.75 - 30,
                                   app.width, app.height * 0.75, "orange", 
                                   app.height * 0.75 - 30)
        app.obstacles.append(triangle)

# Function to check if obstacles have been passed by magic square
# Must check the following conditions: 
# 1. That the x0 coordinate of the square is on the right of the obstacle
# 2. 

def passedObstacle(app, obstacle):
    if ((app.magicSquare.x0 > obstacle.x1)): return True
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

# Must debug this!
def checkCollision(app):
    # Collision happens when x1 of the magicSquare > x0 of the obstacle
    # If the object has passed the obstacle, it is not counted
    for obstacle in app.obstacles:
        if ((app.magicSquare.x1 >= obstacle.x0) and 
            (app.magicSquare.y1 == obstacle.y0) and 
            passedObstacle(app, obstacle) == False):
            app.gameover = True
            return True
    return False

# ------------------------------------------------------------------------------
##########################  SPLASH SCREEN MODE  ################################
# ------------------------------------------------------------------------------


def splashScreenMode_redrawAll(app, canvas):
    # Draw the background
    canvas.create_image(app.width / 2, app.height / 2, 
                        image = ImageTk.PhotoImage(app.splashScreenBackground))

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

    # To check high score

    # To add song


def splashScreenMode_mousePressed(app, event):
    # Mouse Pressed
    cx = event.x
    cy = event.y

    # If mouse pressed in the play button
    playButtonWidthLeft = app.width / 2 - app.splashScreenPlaySmallButton.width
    playButtonWidthRight = app.width / 2 + app.splashScreenPlaySmallButton.width
    playButtonHeightLeft = (app.height / 2 + 30) - app.splashScreenPlaySmallButton.height
    playButtonHeightRight = (app.height / 2 + 30) + app.splashScreenPlaySmallButton.height
    if ((playButtonWidthLeft <= cx <= playButtonWidthRight) and 
        (playButtonHeightLeft <= cy <= playButtonHeightRight)):
        app.mode = 'gameMode'
        # Stop splash screen music
        app.splashScreenMusic.stop()
        # Only start the song when the music has ended
        app.gameMusic.start()

    # If mouse pressed in the high score button
    highScoreButtonWidthLeft = (app.width / 2 + 200) - app.highScoreSmallImage.width
    highScoreButtonWidthRight = (app.width / 2 + 200) + app.highScoreSmallImage.width
    highScoreButtonHeightLeft = (app.height / 2 + 30) - app.highScoreSmallImage.height
    highScoreButtonHeightRight = (app.height / 2 + 30) + app.highScoreSmallImage.height
    if ((highScoreButtonWidthLeft <= cx <= highScoreButtonWidthRight) and 
        (highScoreButtonHeightLeft <= cy <= highScoreButtonHeightRight)):
        app.mode = 'highScore'

    # If mouse pressed in the map pack button

    mapPackButtonWidthLeft = (app.width / 2 - 200) - app.mapPackSmallImage.width
    mapPackButtonWidthRight = (app.width / 2 - 200) + app.mapPackSmallImage.width
    mapPackButtonHeightLeft = (app.height / 2 + 30) - app.mapPackSmallImage.height
    mapPackButtonHeightRight = (app.height / 2 + 30) + app.mapPackSmallImage.height
    if ((mapPackButtonWidthLeft <= cx <= mapPackButtonWidthRight) and 
        (mapPackButtonHeightLeft <= cy <= mapPackButtonHeightRight)):
        app.mode = 'mapPack'

def splashScreenMode_timerFired(app):
    return 42

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
    if app.gameover:
        drawGameOver(app, canvas)

def gameMode_keyPressed(app, event):
    # Jumping
    if event.key == "Space":
        # Can only jump if the square is on the ground or on some object
        if app.isInAir == False:
            app.magicSquare.jump()
            app.isInAir = True

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
    removeObstacle(app)

    # Periodic dropping of the square if the square is above the ground
    if app.magicSquare.y1 < app.ground[2]:
        app.magicSquare.drop()

    if app.magicSquare.y1 == app.ground[2]:
        app.isInAir = False

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
######################         RUNNING THE CODE        #########################
# ------------------------------------------------------------------------------

def playGeometryDash():
    runApp(width = 700, height = 400)

playGeometryDash()