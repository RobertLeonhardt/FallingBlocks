"""
    
    FallingBlocks.py
    Falling Blocks Algorithm Study

    @date:      2019-11-18
    @author:    Robert Leonhardt <mail@4px.io>

"""

# Imports
import sys, pygame, random

# Main game class
class FallingBlocks:

	# Window where all of the elements will be drawn (will be set by initializer)
	MAIN_WINDOW = False

	# Define game window margins
	MAIN_WINDOW_MARGIN_TOP = 100
	MAIN_WINDOW_MARGIN_LEFT = 40

	# Dimension of game grid (will be overwritten by the initializer)
	MAIN_NUM_ROWS = 0
	MAIN_NUM_COLUMNS = 0

	# Element size and margin
	MAIN_BLOCK_SIZE = 20
	MAIN_BLOCK_MARGIN = 2

	# Colors
	COLOR_SCORE_TEXT = (100,140,140)
	COLOR_MAIN_BORDER = (200,200,200)
	COLOR_BLOCK_DEFAULT = (240,240,240)

	# Border thicknesses
	BLOCK_BORDER_MOVABLE = 1
	BLOCK_BORDER_FINAL = 3
	BLOCK_BORDER_FIXED = 0

	# Game block constants
	BLOCK_STATUS, BLOCK_POSITION, BLOCK_COLOR = 0,1,2
	BLOCK_STATUS_MOVABLE, BLOCK_STATUS_FINAL, BLOCK_STATUS_FIXED = 1,2,3

	# Game score
	game_score = 0
	game_highscore = 0

	# Game status
	game_active = False

	# Blocks
	game_blocks = []

	# Last block type (so that there are not two of the same kind following each other)
	game_last_block_set = -1

	# Array with available block sets
	game_block_sets = [ # Square
		[(100,0,0),		[(1,1),(1,2),(2,1),(2,2)]],
		# Bar
		[(0,100,0),		[(1,1),(1,2),(1,3),(1,4)]],
		# Upside-down T
		[(0,0,100),		[(2,1),(1,2),(2,2),(3,2)]],
		# L
		[(100,100,0),	[(1,1),(1,2),(1,3),(2,3)]],
		# L (hor. flipped)
		[(100,0,100),	[(2,1),(2,2),(2,3),(1,3)]],
		# Z
		[(0,100,100),	[(1,1),(2,1),(2,2),(3,2)]],
		# Z (hor. flipped)
		[(50,100,50),	[(2,1),(3,1),(1,2),(2,2)]]]


	# Initializer
	def __init__(self, WINDOW, rows = 20, columns = 10):
		
		# Set window
		self.MAIN_WINDOW = WINDOW

		# Set parameters
		self.MAIN_NUM_ROWS = rows
		self.MAIN_NUM_COLUMNS = columns

		# Start game
		self.start()



	# Start game
	def start(self):

		# Only do this function when game isnt active
		if self.game_active: return False

		# Update status
		self.game_active = True

		# Spawn blocks
		self.spawn_blocks()

		# Update view
		self.update_view()



	# Draw grid
	def draw_grid(self):

		# Calculate main area size
		game_area_width = self.MAIN_NUM_COLUMNS * ( self.MAIN_BLOCK_SIZE + self.MAIN_BLOCK_MARGIN ) + 3 * self.MAIN_BLOCK_MARGIN
		game_area_height = self.MAIN_NUM_ROWS * ( self.MAIN_BLOCK_SIZE + self.MAIN_BLOCK_MARGIN ) + 3 * self.MAIN_BLOCK_MARGIN

		# Draw outer game area border
		pygame.draw.rect(self.MAIN_WINDOW, self.COLOR_MAIN_BORDER, (self.MAIN_WINDOW_MARGIN_LEFT - 2 * self.MAIN_BLOCK_MARGIN, self.MAIN_WINDOW_MARGIN_TOP - 2 * self.MAIN_BLOCK_MARGIN, game_area_width, game_area_height), 1)

		# Iterate through rows
		for row in range(self.MAIN_NUM_ROWS):

			# Iterate through columns
			for column in range(self.MAIN_NUM_COLUMNS):

				# Calculate block coordinates
				x = self.MAIN_WINDOW_MARGIN_LEFT + ( self.MAIN_BLOCK_SIZE + self.MAIN_BLOCK_MARGIN ) * column
				y = self.MAIN_WINDOW_MARGIN_TOP  + ( self.MAIN_BLOCK_SIZE + self.MAIN_BLOCK_MARGIN ) * row

				# Set block color (this will be overwritten, if a block exists)
				color = self.COLOR_BLOCK_DEFAULT

				# Set default border thickness 
				border_width = self.BLOCK_BORDER_MOVABLE

				# Iterate through blocks
				for block in self.game_blocks:

					# Overwrite block color if positions match
					if (column, row) == block[self.BLOCK_POSITION]:

						# Overwrite block color
						color = block[self.BLOCK_COLOR]

						# Check if block is final
						if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FINAL: border_width = self.BLOCK_BORDER_FINAL

						# Check if block is fixed
						if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED: border_width = self.BLOCK_BORDER_FIXED
				
				# Draw elements
				pygame.draw.rect(self.MAIN_WINDOW, color, (x, y, self.MAIN_BLOCK_SIZE, self.MAIN_BLOCK_SIZE), border_width)

		# Set font for score text
		font = pygame.font.SysFont("Helvetica Neue", 30)
		text_score_label = font.render(f"Score:", True, self.COLOR_SCORE_TEXT)
		text_score = font.render(f"{self.game_score}", True, self.COLOR_SCORE_TEXT)
		text_highscore_label = font.render(f"Highscore:", True, self.COLOR_SCORE_TEXT)
		text_highscore = font.render(f"{self.game_highscore}", True, self.COLOR_SCORE_TEXT)
		text_restart = font.render(f"Press S restart!", True, self.COLOR_SCORE_TEXT)

		# Add text to screen
		self.MAIN_WINDOW.blit(text_score_label,(self.MAIN_WINDOW_MARGIN_LEFT,self.MAIN_WINDOW_MARGIN_TOP - 30))
		self.MAIN_WINDOW.blit(text_score,(self.MAIN_WINDOW_MARGIN_LEFT + 120,self.MAIN_WINDOW_MARGIN_TOP - 30))
		self.MAIN_WINDOW.blit(text_highscore_label,(self.MAIN_WINDOW_MARGIN_LEFT,self.MAIN_WINDOW_MARGIN_TOP - 65))
		self.MAIN_WINDOW.blit(text_highscore,(self.MAIN_WINDOW_MARGIN_LEFT + 120,self.MAIN_WINDOW_MARGIN_TOP - 65))

		# Add new game text when game isn't active
		if not self.game_active: self.MAIN_WINDOW.blit(text_restart,(self.MAIN_WINDOW_MARGIN_LEFT + 20,self.MAIN_WINDOW_MARGIN_TOP + 50))



	# Method to spawn blocks
	def spawn_blocks(self):
		
		# Loop as long as there is no "new" block
		while True:

			# Get random block set id
			block_set_id = random.randint(0,len(self.game_block_sets) - 1)

			# Break loop if new block set is not equal to the last one
			if block_set_id != self.game_last_block_set: break

		# Set latest block set
		self.game_last_block_set = block_set_id

		# Get block set
		block_set = self.game_block_sets[block_set_id]

		# Get color
		block_color = block_set[0]

		# Get block positions
		block_positions = block_set[1]

		# Set initial position
		initial_x = random.randint(2,self.MAIN_NUM_COLUMNS - 4)
		initial_y = -1

		# Iterate through all positions
		for (block_rel_pos_x, block_rel_pos_y) in block_positions:

			# Add block
			self.game_blocks.append([self.BLOCK_STATUS_MOVABLE,(initial_x + block_rel_pos_x, initial_y + block_rel_pos_y),block_color])



	# Method for moving blocks
	def move_blocks(self, delta_x, delta_y):

		# Set status flags
		mark_as_final = False
		mark_as_fixed = False

		# Moving in x direction flag
		move_x = True

		# Default positions
		block_pos_x = 0
		block_pos_y = 0

		# Iterate through all blocks
		for block in self.game_blocks:

			# Skip loop iteration if block status is fixed
			if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED: continue

			# Get block position
			(block_pos_x, block_pos_y) = block[self.BLOCK_POSITION]

			# Check if block shall move down and block status
			if not self.position_is_free(block_pos_x + delta_x, block_pos_y + delta_y):

				# Check block status and mark all blocks as final
				if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_MOVABLE and delta_y > 0: mark_as_final = True
					
				# Check block status and mark all blocks as fixed
				if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FINAL and delta_y > 0: mark_as_fixed = True

				# Check if block shall be movable in x direction
				if delta_x > 0: move_x = False

				# Break loop
				break

		# Check if the status of all blocks shall be updated
		if mark_as_final or mark_as_fixed:

			# Iterate through all blocks
			for block in self.game_blocks:

				# Update blocks if they are movable and shall be final
				if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_MOVABLE and mark_as_final: block[self.BLOCK_STATUS] = self.BLOCK_STATUS_FINAL

				# Update blocks if they are final and shall be fixed
				if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FINAL and mark_as_fixed: block[self.BLOCK_STATUS] = self.BLOCK_STATUS_FIXED

		# Print status
		#print(f"Delta: {delta_x}, {delta_y}		PIF: {self.position_is_free(block_pos_x + delta_x, block_pos_y + delta_y)}")

		# Check if space is free
		if self.position_is_free(block_pos_x + delta_x, block_pos_y + delta_y):

			# Iterate through all blocks
			for block in self.game_blocks:

				# Skip loop iteration if block status is fixed
				if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED: continue

				# Get block position
				(block_pos_x, block_pos_y) = block[self.BLOCK_POSITION]

				# Reset delta x if moving in this direction is disbaled
				if not move_x: delta_x = 0

				# Update block positions
				block[self.BLOCK_POSITION] 	= (block_pos_x + delta_x, block_pos_y + delta_y)


		# Check game status if game marked as fixed
		if mark_as_fixed: self.check()

		# Update view
		self.update_view()



	# Function to rotate blocks
	def rotate(self):

		# Counter for non-fixed blocks
		active_block_count = 0

		# Array with position values
		x_values = []
		y_values = []

		# Array with block positions
		current_abs_positions = []
		current_rel_positions = []
		new_abs_positions = []
		
		# Iterate through blocks to get current locations 
		for block in self.game_blocks:

			# Skip loop iteration if block status is fixed
			if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED: continue

			# Update block counter
			active_block_count += 1

			# Get block positions
			(x_pos, y_pos) = block_pos = block[self.BLOCK_POSITION]

			# Add values to array
			x_values.append(x_pos)
			y_values.append(y_pos)

			# Add current position to array
			current_abs_positions.append(block_pos)

		# End function if there arnt any active blocks
		if active_block_count == 0: return False

		# Get max dimensions
		min_x_value = min(x_values, default = 0)
		max_x_value = max(x_values, default = 0)
		min_y_value = min(y_values, default = 0)
		max_y_value = max(y_values, default = 0)

		# Get overal max length
		dimension = max([(max_x_value - min_x_value),(max_y_value - min_y_value)]) + 1

		# Loop through found blocks to convert absolute to relativ positions
		for block_abs_pos_x, block_abs_pos_y in current_abs_positions:

			# Subtract min values and save to var
			current_rel_positions.append((block_abs_pos_x - min_x_value, block_abs_pos_y - min_y_value))

		# Loop through relativ positions to calculate the new ones
		for block_rel_pos_x, block_rel_pos_y in current_rel_positions:

			# Transform coordinates and add to array
			new_abs_positions.append((block_rel_pos_y + min_x_value, -block_rel_pos_x + max_y_value))

		# Define x offset var (-1 neans that there is no way that the transformed block will fit into its destinated position -> dont rotate)
		x_offset = -1

		# Iterate through possible x positions to find a place for the rotated block which than can be checked for free space
		for x_start_offset in range(max_x_value - min_x_value + 1):

			# Flag that positions are free
			position_free = True

			# Iterate through positions to check if theyre free
			for new_pos_x, new_pos_y in new_abs_positions:

				# Set flag to false if a space is not available
				if not self.position_is_free(new_pos_x + x_start_offset, new_pos_y): 

					# Set flag
					position_free = False

					# Break loop
					break

			# If flag is still true, the position is free for all blocks so we can save the position
			if position_free:

				# Update offset
				x_offset = x_start_offset

				# Break loop
				break


		# If there is a way to place the transformed block, write positions
		if x_offset > -1:

			# Set index
			i = 0

			# Iterate through items to change the blocks locations
			for block in self.game_blocks:

				# Skip loop iteration if block status is fixed
				if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED: continue

				# Set new position
				block[self.BLOCK_POSITION] = new_abs_positions[i]

				# Update index
				i += 1

		# Update view
		self.update_view()



	# Method to check the game status
	def check(self):

		# Array with rows that are full
		full_rows_array = []

		# Iterate through all rows to finde full rows
		for row in range(self.MAIN_NUM_ROWS):

			# Flag that row is full
			row_is_full = True

			# Iterate through all columns to check positions
			for column in range(self.MAIN_NUM_COLUMNS):

				# Set flag if a position in this row is free
				if self.position_is_free(column, row): 

					# Set flag
					row_is_full = False

					# Break loop
					break

			# Add row to array if row is full
			if row_is_full: full_rows_array.append(row)

		# Iterate through full rows to actually delete them 
		for i in range(len(full_rows_array) - 0):

			# Get row (from bottom up)
			row = full_rows_array[len(full_rows_array) - 1 - i] + i

			# Temp index
			j = 0

			# Array with blocks that shall be deleted
			blocks_to_delete = []

			# Iterate through all blocks
			for block in self.game_blocks:

				# Get block position
				block_pos_x, block_pos_y 	= block[self.BLOCK_POSITION]

				# Check if y position equals full row
				if block_pos_y == row:

					# Mark block as deleteable
					blocks_to_delete.append(j)

				# Update index
				j += 1

			# Temp index
			j = 0

			# Go through all deletable blocks to actually delete them
			for delete_block in blocks_to_delete:

				# Delete block
				del self.game_blocks[delete_block - j]

				# Update index
				j += 1

			# Iterate through all blocks to move them down
			for block in self.game_blocks:

				# Get block position
				block_pos_x, block_pos_y 	= block[self.BLOCK_POSITION]

				# Check position
				if block_pos_y < row:

					# Move block down
					block[self.BLOCK_POSITION] 	= (block_pos_x, block_pos_y + 1)

		old_score = self.game_score

		# Update score if rows are deleted
		if len(full_rows_array) > 0: 

			# Update score
			self.game_score = old_score + self.MAIN_NUM_COLUMNS ** len(full_rows_array)

			# Print score calculation
			print(f"{old_score} + {self.MAIN_NUM_COLUMNS} ^ {len(full_rows_array)} ({self.MAIN_NUM_COLUMNS ** len(full_rows_array)}) = {old_score + self.MAIN_NUM_COLUMNS ** len(full_rows_array)}")

		# Define var which counts all active blocks
		active_blocks_num = 0

		# Iterate through blocks
		for block in self.game_blocks:

			# Update counter if block is active
			active_blocks_num = active_blocks_num if block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED else active_blocks_num + 1

			# Get block position
			block_pos_x, block_pos_y = block[self.BLOCK_POSITION]

			# If one of the fixed blocks is "touching" the upper border, game is lost
			if block_pos_y <= 0:# and block[self.BLOCK_STATUS] == self.BLOCK_STATUS_FIXED: 

				# Call end game function
				self.end()
				print(100100)

				# Return
				return False

		# If no movable blocks are left, add new blocks
		if active_blocks_num == 0: self.spawn_blocks()



	# End game function
	def end(self):

		# Update status
		self.game_active = False

		# Set scores
		if self.game_score > self.game_highscore: self.game_highscore = self.game_score

		# Reset game score
		self.game_score = 0

		# Remove all blocks
		self.game_blocks = []

		# Update view
		self.update_view()



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



	# Method to check if a positions is free
	def position_is_free(self, x, y):

		# Return false if requested position is simply outside of the game area
		if x < 0 or x > (self.MAIN_NUM_COLUMNS - 1) or y < 0 or y > (self.MAIN_NUM_ROWS - 1): return False
		
		# Iterate through all blocks
		for block in self.game_blocks:

			# Skip loop iteration if block status (only consider fixed blocks)
			if block[self.BLOCK_STATUS] != self.BLOCK_STATUS_FIXED: continue

			# Return false if position equals requested position
			if (x, y) == block[self.BLOCK_POSITION]: return False

		# No other returns until now, return true
		return True



	# Refresh screen
	def update_view(self):

		# Clear screen
		self.MAIN_WINDOW.fill((255,255,255))

		# Draw grid
		self.draw_grid()
