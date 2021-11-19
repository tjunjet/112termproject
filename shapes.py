import time
import math

# Main moving block
class magicSquare(object):
    def __init__(self, width, height, color, centerX, centerY):
        self.width = width
        self.height = height
        self.color = color
        self.centerX = centerX
        self.centerY = centerY
        self.x0 = centerX - width / 2
        self.x1 = centerX + width / 2
        self.y0 = centerY - height / 2
        self.y1 = centerY + height / 2
        self.dt = 5
        self.angularFrequency = math.pi / self.dt

    # Getting the time taken for the square to jump across an obstacle
    # def get_time(self, time):
    #     self.time = time

    # Making square jump. But based on physics
    def jump(self):
        # Physics values
        # This displacement value can be configured whenever you want.
        displacement = 60

        # Initial Jump
        self.centerY -= displacement
        self.y0 = self.centerY - self.height / 2
        self.y1 = self.centerY + self.height / 2

        # Dropping. While loop runs until displacement 0
        # Must calculate time elapsed
        # count = 0
        # while displacement > 0:
        #     time2 = time.time()
        #     # Making sure that every 10 seconds, the square will fall
        #     if (time2 - time1) % gravity == 0:
        #         self.centerY += gravity
        #         self.y0 = self.centerY - self.height / 2
        #         self.y1 = self.centerY + self.height / 2
        #         displacement -= gravity

    def land(self):
        self.centerY += 60
        self.y0 = self.centerY - self.height / 2
        self.y1 = self.centerY + self.height / 2

    def fly(self):
        return 42

    # Constant rotating of the square
    def rotate(self):
        return 42

    # Constant dropping of the square based on gravity
    # Every timer fired, we call a drop on the square
    def drop(self):
        self.centerY += 3
        self.y0 = self.centerY - self.height / 2
        self.y1 = self.centerY + self.height / 2

    def teleport(self, ground, ceiling):
        if self.y1 == ground[2]:
            self.y0 = ceiling[2]
            self.y1 = ceiling[2] + self.height

        else:
            self.y0 = ground[2] - self.height
            self.y1 = ground[2]

# Obstacles
class Square(object):
    def __init__(self, x0, y0, x1, y1, color):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.color = color

# Triangle 
class Triangle(object):
    def __init__(self, x0, y0, x1, y1, x2, y2, color, height):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        self.y0 = y0
        self.y1 = y1
        self.y2 = y2
        self.color = color
        self.height = height

# Portals for teleportation
class Portal(object):
    # cx and cy are the coordinates of the center of the portal
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy

# Reverse Gravity Mode obstacles
class Rectangle(object):
    def __init__(self, cx, cy, height, width):
        self.cx = cx
        self.cy = cy
        self.height = height
        self.width = width
        self.x0 = self.cx - width / 2
        self.x1 = self.cx + width / 2
        self.y0 = self.cy - height / 2
        self.y1 = self.cy + height / 2

# AntiGravity Mode obstacle
class bigTriangle(object):
    def __init__(self):
        return

