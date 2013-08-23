import curses

class Level:
	def __init__(self):
		# N = wall
		# o = power pellet
		# . = pellet 
		# g = ghost
		# _ = ghost gate
		# p = pacan spawn
		self.tile = [
				"NNNNNNNNNNNNNNNN",
				"No.............N",
				"N.NNNNNN.NNNNN.N",
				"N........NNNNN.N",
				"NNNNNNNN.NNNNN.N",
				"N..............N",
				"N.NNNNN_NNNNNN.N",
				"N.....NgNNNNNN.N",
				"N.NNN.NNNN.....N",
				"N.NNN.NNNN.NNNNN",
				"N.......pN.....N",
				"NNNNNNNN.N.NNN.N",
				"N..........NNN.N",
				"N.NNNNNN.N.NNN.N",
				"No.......N....oN",
				"NNNNNNNNNNNNNNNN"
				]
		self.height = 16
		self.width = 16
		self.pellets = 0
		for y in range(self.height):
			for x in range(self.width):
				if self.tile[y][x] == 'p':
					self.player_spawn = (y,x)
				elif self.tile[y][x] == 'g':
					self.ghost_spawn = (y,x)
				elif self.tile[y][x] == '.':
					self.pellets += 1
	def get_tile(self, y, x):
		return (self.tile[y][x])
	def set_tile(self, y, x, new):
		new_row = self.tile[y]
		new_row = new_row[0:x] + new + new_row[x+1:]
		self.tile[y] = new_row
	def draw(self, screen):
		screen.move(0,0)
		for y in range(self.height):
			for x in range(self.width):
				if self.tile[y][x] == 'N':
					screen.addstr(y,x,"X",curses.color_pair(1))
				elif self.tile[y][x] == 'o':
					screen.addstr(y,x,'o',curses.color_pair(2))
				elif self.tile[y][x] == '.':
					screen.addstr(y,x,'.',curses.color_pair(3))
				elif self.tile[y][x] == '_':
					screen.addstr(y,x,'_',curses.color_pair(4))
				else:
					screen.addstr(y,x,' ',curses.color_pair(8))
