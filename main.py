"""
    
    main.py
    Falling Blocks Algorithm Study

    @date:      2019-11-10
    @author:    Robert Leonhardt <mail@4px.io>

"""

# Imports
import sys, pygame
from FallingBlocks import FallingBlocks

# Init pygame
pygame.init()

# Define window 
WINDOW_HEIGHT               = 600
WINDOW_WIDTH                = 300
WINDOW_SIZE                 = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_TITLE                = "Falling Blocks Algorithm Study"

# Define colors
COLOR_MAIN_BACKGROUND       = (255,255,255)

# Define screen
WINDOW                      = pygame.display.set_mode(WINDOW_SIZE)

# Set title
pygame.display.set_caption(WINDOW_TITLE)

# Set background color
WINDOW.fill(COLOR_MAIN_BACKGROUND)

# Init game
falling_blocks  = FallingBlocks(WINDOW)

# Setup clock
clock = pygame.time.Clock()

# Set time elapsed
time_elapsed = 0

# Loop so the window doesnt close
while True:
   
    # Get event
    for event in pygame.event.get():

        # Exit window when c button is clicked
        if event.type == pygame.QUIT: sys.exit()

        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:

            # KEY UP
            if event.key == pygame.K_UP: falling_blocks.rotate_block()

            # DOWN KEY
            if event.key == pygame.K_DOWN: falling_blocks.step_down()

            # LEFT KEY
            if event.key == pygame.K_LEFT: falling_blocks.step_left()

            # RIGHT KEY
            if event.key == pygame.K_RIGHT: falling_blocks.step_right()

    # Calc time since last click
    time_elapsed += clock.tick()

    # If time elapsed greater than a second, update game
    if time_elapsed >= 1000:

        # Move down
        #falling_blocks.step_down()   

        # Reset time elapsed
        time_elapsed = 0       


    # Clean up view
    pygame.display.flip()