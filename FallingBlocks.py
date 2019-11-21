"""
    
    FallingBlocks.py
    Falling Blocks Algorithm Study

    @date:      2019-11-10
    @author:    Robert Leonhardt <mail@4px.io>

"""

# Imports
import sys, pygame, random

# Main game class
class FallingBlocks:

	# Internal constants
	BLOCK_TYPE, BLOCK_STATUS, BLOCK_POSITION, BLOCK_COLOR, BLOCK_REL_POSITION, BLOCK_ROTATABLE = 0, 1, 2, 3, 4, 5

	# Window where all of the elements will be drawn (will be set by initializer)
	WINDOW 						= False

	# Define game window margins
	WINDOW_MARGIN_TOP 			= 100
	WINDOW_MARGIN_LEFT 			= 40

	# Dimension of game grid (will be overwritten by the initializer)
	MAIN_NUM_ROWS 				= 0
	MAIN_NUM_COLUMNS 			= 0

	# Define colors
	COLOR_MAIN_BORDER 			= (100,100,100)
	COLOR_BLOCK_DEFAULT 		= (240,240,240)
	COLOR_BLOCK_1 				= (110,220,255)
	COLOR_BLOCK_2 				= (210,120,55)
	COLOR_BLOCK_3 				= (10,120,35)
	COLOR_BLOCK_4 				= (110,220,85)
	COLOR_BLOCK_5 				= (210,20,155)

	# Var for last block type
	last_block_type 			= 0

	# Game flag
	game_active 				= False

	# Blocks can move left/right/down
	game_block_almost_bottom 	= False

	# Element size and margin
	block_size 					= 20
	block_margin 				= 2

	# Array with blocks
	blocks 						= []



	# Initializer
	def __init__(self, WINDOW, rows = 20, columns = 10):
		
		# Set window
		self.WINDOW 			= WINDOW

		# Set parameters
		self.MAIN_NUM_ROWS 		= rows
		self.MAIN_NUM_COLUMNS 	= columns

		# Start game
		self.start()



	# Start game
	def start(self):

		# Set game flag
		self.game_active = True

		# Set first block
		self.add_block_group()

		# Draw grid
		self.draw_grid()



	# Draw grid
	def draw_grid(self):

		# Calculate main area size
		game_area_width 	= self.MAIN_NUM_COLUMNS * ( self.block_size + self.block_margin ) + 3 * self.block_margin
		game_area_height 	= self.MAIN_NUM_ROWS * ( self.block_size + self.block_margin ) + 3 * self.block_margin

		# Draw outer border
		pygame.draw.rect(self.WINDOW, self.COLOR_MAIN_BORDER, (self.WINDOW_MARGIN_LEFT - 2 * self.block_margin, self.WINDOW_MARGIN_TOP - 2 * self.block_margin, game_area_width, game_area_height), 1)

		# Iterate through rows
		for row in range(self.MAIN_NUM_ROWS):

			# Iterate through columns
			for column in range(self.MAIN_NUM_COLUMNS):

				# Calculate block coordinates
				x 		= self.WINDOW_MARGIN_LEFT + ( self.block_size + self.block_margin ) * column
				y 		= self.WINDOW_MARGIN_TOP + ( self.block_size + self.block_margin ) * row

				# Set block color (this will be overwritten, if a block exists)
				color 	= self.COLOR_BLOCK_DEFAULT

				# Check blocks
				for block in self.blocks:

					# Check if current position equals block position
					if (column, row) == block[self.BLOCK_POSITION]:

						# Overwrite color
						color = block[self.BLOCK_COLOR]
				
				# Draw elements
				pygame.draw.rect(self.WINDOW, color, (x, y, self.block_size, self.block_size), 0)



	# Add block group method
	def add_block_group(self):

		# Temporary flag
		flag = True

		# While there is new block until the last one
		while flag:

			# Get random block number
			block = random.randint(1,5)

			# If the new generated block is NOT the same as the last one, stop 
			if block != self.last_block_type:

				# Save block type
				self.last_block_type = block

				# Leave the loop
				flag = False

		# Block 1
		if block == 1:

			# Create block
			self.blocks.append([1,1,(2,0),self.COLOR_BLOCK_1,(1,1),True])
			self.blocks.append([1,1,(3,0),self.COLOR_BLOCK_1,(1,2),True])
			self.blocks.append([1,1,(3,1),self.COLOR_BLOCK_1,(2,2),True])
			self.blocks.append([1,1,(3,2),self.COLOR_BLOCK_1,(3,2),True])
			self.blocks.append([1,1,(4,2),self.COLOR_BLOCK_1,(3,3),True])

		# Block 2
		if block == 2:

			# Create block
			self.blocks.append([1,1,(2,0),self.COLOR_BLOCK_2,(1,1),True])
			self.blocks.append([1,1,(2,1),self.COLOR_BLOCK_2,(2,1),True])
			self.blocks.append([1,1,(2,2),self.COLOR_BLOCK_2,(3,1),True])
			self.blocks.append([1,1,(3,2),self.COLOR_BLOCK_2,(3,2),True])

		# Block 3
		if block == 3:

			# Create block
			self.blocks.append([1,1,(2,0),self.COLOR_BLOCK_3,(1,2),True])
			self.blocks.append([1,1,(2,1),self.COLOR_BLOCK_3,(2,2),True])
			self.blocks.append([1,1,(2,2),self.COLOR_BLOCK_3,(3,2),True])

		# Block 4
		if block == 4:

			# Create block
			self.blocks.append([1,1,(3,0),self.COLOR_BLOCK_4,(1,2),True])
			self.blocks.append([1,1,(2,1),self.COLOR_BLOCK_4,(2,1),True])
			self.blocks.append([1,1,(3,1),self.COLOR_BLOCK_4,(2,2),True])
			self.blocks.append([1,1,(4,1),self.COLOR_BLOCK_4,(2,3),True])
			self.blocks.append([1,1,(3,2),self.COLOR_BLOCK_4,(3,2),True])

		# Block 5
		if block == 5:

			# Create block
			self.blocks.append([1,1,(2,0),self.COLOR_BLOCK_5,(1,1),False])
			self.blocks.append([1,1,(2,1),self.COLOR_BLOCK_5,(2,1),False])
			self.blocks.append([1,1,(3,0),self.COLOR_BLOCK_5,(1,2),False])
			self.blocks.append([1,1,(3,1),self.COLOR_BLOCK_5,(2,2),False])



	# Method to get the information if a specific position is free
	def position_is_free(self, x, y):

		# Go through blocks to 
		for block in self.blocks:

			# Get block position
			(block_position_x, block_position_y) 	= block[self.BLOCK_POSITION]

			# Check if block position matches the requested position
			if ( block_position_x == x and block_position_y == y and block[self.BLOCK_STATUS] == 2 ) or x == -1 or x == self.MAIN_NUM_COLUMNS or y == self.MAIN_NUM_ROWS:

				# Space is occupied or not available
				return False

		# Space is not occupied
		return True



	# Moving blocks position
	def move_blocks(self, delta_x, delta_y):

		# Flag for moving blocks
		move_blocks_x 	= True
		move_blocks_y 	= True

		# Flag for fixing all blocks
		fix_all_blocks 	= False

		# Iterate through blocks
		for block in self.blocks:

			# Check for movable blocks
			if block[self.BLOCK_STATUS] == 1:

				# Get position
				(block_position_x, block_position_y) = block[self.BLOCK_POSITION]

				# Deactive moving in x direction if next block is not free
				if not self.position_is_free(block_position_x + delta_x, block_position_y): move_blocks_x = False

				# Check if y-direction is not available
				if not self.position_is_free(block_position_x, block_position_y + delta_y): 

					# Check if there is the possibility to move the block in x direction (when y positions is not available for the first time)
					if not self.game_block_almost_bottom:

						# Block is now almost at the bottom, next y movement will cause all blocks to be fixed
						self.game_block_almost_bottom 	= True

						# No further movement in y direction
						move_blocks_y 					= False

					else:

						# Block is already as for as possible in y direction, fix all blocks
						fix_all_blocks = True

		# Iterate through blocks to acutally move them
		for block in self.blocks:

			# Fix all blocks if flag is set
			if fix_all_blocks: block[self.BLOCK_STATUS] = 2

			# Check for movable blocks
			if block[self.BLOCK_STATUS] == 1:

				# Get position
				(block_position_x, block_position_y) 	= block[self.BLOCK_POSITION]

				# No movement in x direction if disabled
				if not move_blocks_x: delta_x = 0

				# No movement in y direction if disabled
				if not move_blocks_y: delta_y = 0

				# Check if block will move in y direction and Reset almost bottom flag
				if delta_y > 0: self.game_block_almost_bottom = False

				# Move block
				block[self.BLOCK_POSITION] 				= (block_position_x + delta_x, block_position_y + delta_y)
		
				# Set flag, if next y position isnt free
				if self.position_is_free(block_position_x, block_position_y + delta_y): self.game_block_almost_bottom = True

		# Add new block if all other blocks got fixed recently
		if fix_all_blocks: self.add_block_group()						

		# Clear screen
		self.WINDOW.fill((255,255,255))

		# Update display
		self.draw_grid()



	# Step down method
	def step_down(self):
		# Call move method
		self.move_blocks(0,1)



	# Step left method
	def step_left(self):
		# Call move method
		self.move_blocks(-1,0)



	# Step right method
	def step_right(self):
		# Call move method
		self.move_blocks(1,0)



	# Method for rotating blocks
	def rotate_block(self):

		# Array with x positions
		x_positions 	= []

		# Iterate through blocks to get max and min x position
		for block in self.blocks:

			# Get current location
			(block_position_x, block_position_y) 	= block[self.BLOCK_POSITION]

			# Add position to array
			x_positions.append(block_position_x)

		# Iterate through blocks
		for block in self.blocks:

			# Get current location
			(block_position_x, block_position_y) 	= block[self.BLOCK_POSITION]

			# Get relative position
			(block_rel_row, block_rel_column) 		= block[self.BLOCK_REL_POSITION]

			# Check for movable blocks
			if block[self.BLOCK_STATUS] == 1 and block[self.BLOCK_ROTATABLE] and self.position_is_free(min(x_positions) - 1, block_position_y) and self.position_is_free(max(x_positions) + 1,block_position_y): #and self.position_is_free(block_position_x - block_rel_column, block_position_y) and self.position_is_free(block_position_x + (4 - block_rel_column), block_position_y) and self.position_is_free(block_position_x, block_position_y + (4 - block_rel_column)):

				# Set position dependend on relative location
				if block[self.BLOCK_REL_POSITION] == (1,1): 
					block[self.BLOCK_POSITION] 		= (block_position_x + 0, block_position_y + 2)
					block[self.BLOCK_REL_POSITION] 	= (3,1) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (1,2): 
					block[self.BLOCK_POSITION] 		= (block_position_x - 1, block_position_y + 1)
					block[self.BLOCK_REL_POSITION] 	= (2,1) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (1,3): 
					block[self.BLOCK_POSITION] 		= (block_position_x - 2, block_position_y + 0)
					block[self.BLOCK_REL_POSITION] 	= (1,1) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (2,1): 
					block[self.BLOCK_POSITION] 		= (block_position_x + 1, block_position_y + 1)
					block[self.BLOCK_REL_POSITION] 	= (3,2) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (2,2): 
					block[self.BLOCK_POSITION] 		= (block_position_x + 0, block_position_y + 0)
					block[self.BLOCK_REL_POSITION] 	= (2,2) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (2,3): 
					block[self.BLOCK_POSITION] 		= (block_position_x - 1, block_position_y - 1)
					block[self.BLOCK_REL_POSITION] 	= (1,2) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (3,1): 
					block[self.BLOCK_POSITION] 		= (block_position_x + 2, block_position_y + 0)
					block[self.BLOCK_REL_POSITION] 	= (3,3) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (3,2): 
					block[self.BLOCK_POSITION] 		= (block_position_x + 1, block_position_y - 1)
					block[self.BLOCK_REL_POSITION] 	= (2,3) 
					continue
				
				if block[self.BLOCK_REL_POSITION] == (3,3): 
					block[self.BLOCK_POSITION] 		= (block_position_x + 0, block_position_y - 2)
					block[self.BLOCK_REL_POSITION] 	= (1,3) 
					continue
					

		# Clear screen
		self.WINDOW.fill((255,255,255))

		# Update display
		self.draw_grid()
















