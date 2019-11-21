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
WINDOW_TITLE                = "Falling Blocks Algorithm Study"

# Define colors
COLOR_MAIN_BACKGROUND       = (255,255,255)

# Define screen
WINDOW                      = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set title
pygame.display.set_caption(WINDOW_TITLE)

# Set background color
WINDOW.fill(COLOR_MAIN_BACKGROUND)

# Init game
falling_blocks              = FallingBlocks(WINDOW)

# Setup clock
clock 			            = pygame.time.Clock()

# Set time elapsed
time_elapsed 	            = 0

# Loop so the window doesnt close
while True:
   
    # Get event
    for event in pygame.event.get():

        # Exit window when c button is clicked
        if event.type == pygame.QUIT: sys.exit()

        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:

            # KEY UP - Rotate all movable blocks
            if event.key == pygame.K_UP: 	falling_blocks.rotate()

            # DOWN KEY - Move movable blocks down
            if event.key == pygame.K_DOWN: 	falling_blocks.step_down()

            # LEFT KEY - Move movable blocks to left
            if event.key == pygame.K_LEFT: 	falling_blocks.step_left()

            # RIGHT KEYs - Move movable blocks to right
            if event.key == pygame.K_RIGHT: falling_blocks.step_right()

            # S KEY -  Start new game (when game is lost)
            if event.key == pygame.K_s: 	falling_blocks.start()

    # Calc time since last click
    time_elapsed += clock.tick()

    # If time elapsed greater than a second, update game
    if time_elapsed >= 800:

        # Move down
        falling_blocks.step_down()   

        # Reset time elapsed
        time_elapsed = 0     

    # Clean up view
    pygame.display.flip()
