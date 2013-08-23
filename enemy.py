import curses

class Enemy:
	def __init__(self, level):
		self.symbol = '#'
		self.direction = "none"
		self.dead = False
		self.x, self.y = level.ghost_spawn
		self.scared = False
		self.scared_reset = 15
		self.scared_moves = self.scared_reset
		self.chase = False # chase player or just wander
		self.chase_reset = 15 # moves until mode change
		self.chase_moves = self.chase_reset # keep track of moves 

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
		if self.scared:
			screen.addstr(self.y, self.x, self.symbol, curses.color_pair(1))
		elif self.chase:
			screen.addstr(self.y, self.x, self.symbol, curses.color_pair(6))
		elif not(self.chase):
			screen.addstr(self.y, self.x, self.symbol, curses.color_pair(8))
