import curses

class Player:
	def __init__(self, level):
		self.direction = "none"
		self.lives = 3
		self.dead = False
		self.x, self.y = level.player_spawn
		self.score = 0
		self.power_mode = 0 # 1 means eat ghosts!
		self.power_time = 10 # moves until power mode runs out
	def move(self):
		if self.direction == "left":
			self.x -= 1
		elif self.direction == "right":
			self.x += 1
		elif self.direction == "up":
			self.y -= 1
		elif self.direction == "down":
			self.y += 1

	def draw(self, screen):
		screen.addstr(self.y, self.x, "@", curses.color_pair(5))
