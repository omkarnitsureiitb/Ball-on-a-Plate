import pygame
import numpy as np
import Control as c


# initialising the window. You can ignore this part.

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 40)

# setting plate parameters

centerX = 400
centerY = 400
plateT = 60


r = 0.1 # the radius of the ball

# loading in images and transforming them to required sixes and angles. You can ignore this part.

plate = pygame.image.load("plate.png")
plate = pygame.transform.rotate(plate, -45)
ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, (40, 40))
pivot = pygame.image.load("plain-triangle.png")


# game control variable. This variable determines if the came continues to run. You can ignore this part.

run = True


# A function used to rotate an image about its center. You can ignore this part.
def blit_rot_center(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)


# initialising game parameters

theta = 0       # the variable stores the angle of the plate with the
                # horizontal and measured positive counterclockwise.

phi = 0         # the variable stores the angle of rotation
                # of the ball about its own axis.

x = 0           # the variable stores the distance of
                # the center of the ball form the pivot.

XV = [0,0]      #Initial position and velocity vector

xf = 0          #Final distance of the centre of the ball from the pivot

integral = 0    #Initial value of the integral term

time = 0       #Time spent in the while loop

error = xf      #initial error in the control system


# Game loop
while run:

    # checking for mouse input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                X, Y = event.pos  # gets the x and y coordinates of the mouse left click
                xf = X - centerX    #getting the final x-coordinate that needs to be achieved by the ball
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                X, Y = event.pos  # gets the x and y coordinates of the mouse left click and moving.

    # This is your major task. Write a function which takes in
    # any number of parameters you like and output the new system
    # variables and any other parameter you would like to track.

    updated_values = c.solve( xf, XV, integral, error, theta, time)

    dx = updated_values[0]               #Updated values of all the parameters

    integral = updated_values[1]

    theta = updated_values[2]

    XV = updated_values[3]

    x = updated_values[3][0]

    velocity = updated_values[3][1]

    error = updated_values[4]

    time = updated_values[5]

    # make sure the ball rotates
    dphi = dx / r
    phi += dphi
    # setting the background colour of the screen
    screen.fill((235, 62, 74))

    # displaying the images on the screen within appropriate physical parameters,
    # for example, it is ensured that the ball is always on the plate.

    blit_rot_center(screen, plate, (centerX - 364, centerY - 364), theta)
    blit_rot_center(screen, ball, (centerX - 20 + x * np.cos(np.radians(theta)) - plateT * np.sin(np.radians(theta)),
                                   centerY - 20 - plateT * np.cos(np.radians(theta)) - x * np.sin(np.radians(theta))),
                    -phi)
    screen.blit(pivot, (centerX - 32, centerY - 32 + plateT))

    pygame.display.update()
