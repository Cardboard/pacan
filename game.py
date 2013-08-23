import curses
import random

import pygame # for music

import player
import enemy
import level

class Game:
	def __init__(self):
		# set up curses window
		self.scr = curses.initscr()
		curses.start_color()
		curses.noecho()
		#curses.halfdelay(2)
		self.scr.keypad(1)
		curses.curs_set(0)
		# game variables
		self.running = True
		self.ghost_timer_reset = 15 # number of moves until next ghost spawns
		self.ghost_timer = self.ghost_timer_reset
		# music
		#pygame.init()
		#pygame.mixer.init()
		#pygame.mixer.music.load("pacan.ogg")
		#pygame.mixer.music.play()
		# set up color pairs
		bg = curses.COLOR_BLACK
		curses.init_pair(1, curses.COLOR_BLUE, bg)
		curses.init_pair(2, curses.COLOR_GREEN, bg) 
		curses.init_pair(3, curses.COLOR_CYAN, bg)
		curses.init_pair(4, curses.COLOR_RED, bg)
		curses.init_pair(5, curses.COLOR_YELLOW, bg)
		curses.init_pair(6, curses.COLOR_MAGENTA, bg)
		curses.init_pair(8, curses.COLOR_WHITE, bg)
		# external
		self.level = level.Level()
		self.player = player.Player(self.level)
		self.ghosts = [enemy.Enemy(self.level)]
		# draw the level initially
		self.draw()
	def end(self, quit_message="GAME OVER"):
		# stop running
		self.running = False
		# set window back to normal
		curses.nocbreak()
		self.scr.keypad(0)
		curses.echo()
		curses.endwin()
		del self.scr
		print(quit_message)
		print("SCORE: {}".format(self.player.score))
	def update(self):
		# check for keyboard input
		key = self.scr.getch()
		# exit
		if key == curses.KEY_F2:
			self.end()
		# ghost spawning
		if len(self.ghosts) != 4:
			if self.ghost_timer == 0:
				self.ghosts.append(enemy.Enemy(self.level))
				self.ghost_timer = self.ghost_timer_reset
			else:
				self.ghost_timer -= 1
		self.update_player(key)
		self.update_ghosts(self.player)
		# check if the player collected all the pellets
		if self.level.pellets == 0:
			self.end('YOU WON!')
		# game over if player runs out of lives
		if self.player.lives == 0:
			self.end()
		try:
			self.draw()
		except AttributeError: # thrown after window is deleted
			print("Thanks for playing!")
	
	def draw(self):
		self.draw_info()
		self.level.draw(self.scr)
		for ghost in self.ghosts:
			ghost.draw(self.scr)
		self.player.draw(self.scr)
		self.scr.refresh()

	def run(self):
		while self.running:
			self.update()

	def update_ghosts(self, player):
		# move out of spawn
		for ghost in self.ghosts:
			try:
				if ghost.scared_moves == 0:
					ghost.scared = False
					ghost.scared_moves = ghost.scared_reset
				elif ghost.scared:
					ghost.scared_moves -= 1
				elif not(ghost.scared):
					# change modes occasionally
					if ghost.chase_moves == 0:
						if not(ghost.chase):
							ghost.chase = True
							ghost.chase_moves = ghost.chase_reset
						else:
							ghost.chase = False
							ghost.chase_moves = ghost.chase_reset
					else:
						ghost.chase_moves -= 1
				gpos = (ghost.y, ghost.x)
				if gpos == self.level.ghost_spawn:
					ghost.direction = "up"
				# CHECK FOR COLLISIONS
				# get tile on all sides of the player
				tile_on = self.level.get_tile(ghost.y, ghost.x)
				tile_right = self.level.get_tile(ghost.y, ghost.x+1)
				tile_left = self.level.get_tile(ghost.y, ghost.x-1)
				tile_up = self.level.get_tile(ghost.y-1, ghost.x)
				tile_down = self.level.get_tile(ghost.y+1, ghost.x)
				# ghost path finding
				if ghost.direction == "left":
					# chase after player at each intersection or wall
					if ghost.chase:
						if player.y > ghost.y and tile_down != "N":
							ghost.direction = "down"
						elif player.y < ghost.y and tile_up != "N":
							ghost.direction = "up"
					if ghost.scared:
						if player.y > ghost.y and tile_down != "N":
							ghost.direction = "up"
						elif player.y < ghost.y and tile_up != "N":
							ghost.direction = "down"
					# collide with a wall
					if tile_left == "N":
						# wall above
						if tile_up == "N":
							ghost.direction = "down"
						# wall below
						elif tile_down == "N":
							ghost.direction = "up"
						# no wall above or below
						else:
							ghost.direction = random.choice(["up", "down"])
				elif ghost.direction == "right":
					# chase after player at each intersection or wall
					if ghost.chase:
						if player.y > ghost.y and tile_down != "N":
							ghost.direction = "down"
						elif player.y < ghost.y and tile_up != "N":
							ghost.direction = "up"
					if ghost.scared:
						if player.y > ghost.y and tile_down != "N":
							ghost.direction = "up"
						elif player.y < ghost.y and tile_up != "N":
							ghost.direction = "down"
					# collide with a wall
					if tile_right == "N":
						# wall above 
						if tile_up == "N":
							ghost.direction = "down"
						# wall below
						elif tile_down == "N":
							ghost.direction = "up"
						# no wall above or below
						else:
							ghost.direction = random.choice(["up", "down"])
				elif ghost.direction == "up":
					# chase after player at each intersection or wall
					if ghost.chase:
						if player.x > ghost.x and tile_right != "N":
							ghost.direction = "right"
						elif player.x < ghost.x and tile_left != "N":
							ghost.direction = "left"
					if ghost.scared:
						if player.x > ghost.x and tile_right != "N":
							ghost.direction = "left"
						elif player.x < ghost.x and tile_left != "N":
							ghost.direction = "right"
					# collide with a wall
					if tile_up == "N":
						# wall left 
						if tile_left == "N":
							ghost.direction = "right"
						# wall right 
						elif tile_right == "N":
							ghost.direction = "left"
						# no tile left or right
						else:
							ghost.direction = random.choice(["left", "right"])
				elif ghost.direction == "down":
					# chase after player at each intersection or wall
					if ghost.chase:
						if player.x > ghost.x and tile_right != "N":
							ghost.direction = "right"
						elif player.x < ghost.x and tile_left != "N":
							ghost.direction = "left"
					if ghost.scared:
						if player.x > ghost.x and tile_right != "N":
							ghost.direction = "left"
						elif player.x < ghost.x and tile_left != "N":
							ghost.direction = "right"
					# collide with a wall
					if tile_down == "N":
						# wall left 
						if tile_left == "N":
							ghost.direction = "right"
						# wall right 
						elif tile_right == "N":
							ghost.direction = "left"
						# no tile left or right
						else:
							ghost.direction = random.choice(["left", "right"])

				ghost.move()

				if gpos == (player.y, player.x) or (ghost.x == player.x and ghost.y == player.y):
					if ghost.scared:
						self.player.score += 10
					else:
						self.player.lives -= 1
						self.player.score -= 10
					self.ghosts.remove(ghost)
			# occurs when ghost is deleted?
			except IndexError:
				pass

	def update_player(self, key):
		# get tile on all sides of the player
		tile_on = self.level.get_tile(self.player.y, self.player.x)
		tile_right = self.level.get_tile(self.player.y, self.player.x+1)
		tile_left = self.level.get_tile(self.player.y, self.player.x-1)
		tile_up = self.level.get_tile(self.player.y-1, self.player.x)
		tile_down = self.level.get_tile(self.player.y+1, self.player.x)
		# change direction on keypress
		if key == curses.KEY_LEFT:
			self.player.direction = "left"
		if key == curses.KEY_RIGHT:
			self.player.direction = "right"
		if key == curses.KEY_UP:
			self.player.direction = "up"
		if key == curses.KEY_DOWN:
			self.player.direction = "down"
		# stop moving if hit a wall
		if (self.player.direction == "left" and tile_left == 'N')\
				or (self.player.direction == "right" and tile_right == 'N')\
				or (self.player.direction == "up" and tile_up == 'N')\
				or (self.player.direction == "down" and tile_down == 'N'):
			self.player.direction == "none"
		else:
			# on a pellet
			if tile_on == '.':
				self.level.set_tile(self.player.y, self.player.x, '*')
				self.player.score += 1
				self.level.pellets -= 1
			# on a power pellet
			if tile_on == 'o':
				# POWER MODE!
				self.level.set_tile(self.player.y, self.player.x, ' ')
				self.player.power_mode = self.player.power_time
				for ghost in self.ghosts:
					ghost.scared = True

			self.player.move()

	def draw_info(self):
		# draw name of game
		self.scr.addstr(0, self.level.width + 2, "=PACAN=", curses.color_pair(5))
		# draw score
		score = "SCORE: " + str(self.player.score)
		self.scr.addstr(2, self.level.width + 2, score, curses.color_pair(1))
		# draw remaining lives
		lives = "LIVES: " + str(self.player.lives)
		self.scr.addstr(3, self.level.width + 2, lives, curses.color_pair(1))
		# draw how to play
		controls1 = "CONTROLS:"
		controls2 = "move: arrow keys"
		controls3 = "quit: F2"
		self.scr.addstr(5, self.level.width + 2, controls1, curses.color_pair(2))
		self.scr.addstr(6, self.level.width + 2, controls2, curses.color_pair(2))
		self.scr.addstr(7, self.level.width + 2, controls3, curses.color_pair(2))


