import random, copy
from User.define_user import User
from Grid.define_maze import define_Maze

class define_Grid:
	def __init__(self, gridSize):
		self.gridSize = gridSize
		self.mazeSize = 15
		self.boxSize = 1

		self.displaymazeSize = 9
		if self.displaymazeSize < self.mazeSize:
			self.displayChunk = 3
		else:
			self.displayChunk = int(self.displaymazeSize / self.mazeSize * 3)
			if self.displayChunk % 2 == 0:
				self.displayChunk += 1
		self.wallWidth = (9 / self.displaymazeSize) / 20
		
		self.mapdisplaymazeSize = 31
		if self.mapdisplaymazeSize < self.mazeSize:
			self.mapdisplayChunk = 3
		else:
			self.mapdisplayChunk = int(self.mapdisplaymazeSize / self.mazeSize * 3)
			if self.mapdisplayChunk % 2 == 0:
				self.mapdisplayChunk += 1
		self.mapwallWidth = (9 / self.mapdisplaymazeSize) / 20

		self.grid = []
		for row in range(self.gridSize):
			self.grid.append([])
			for column in range(self.gridSize):
				self.grid[row].append(None)
		self.create_exit()

	def cut_chunkWalls(self, position):
		maze = self.grid[position[1]][position[0]].maze
		if position[0] % 2 == position[1] % 2:
			if position[1] != self.gridSize - 1:
				maze[self.mazeSize - 1][self.mazeSize - 1][0] = 0
			if position[1] != 0:
				maze[0][0][1] = 0
			if position[0] != 0:
				maze[self.mazeSize - 1][0][2] = 0
			if position[0] != self.gridSize - 1:
				maze[0][self.mazeSize - 1][3] = 0
		else:
			if position[1] != self.gridSize - 1:
				maze[self.mazeSize - 1][0][0] = 0
			if position[1] != 0:
				maze[0][self.mazeSize - 1][1] = 0
			if position[0] != 0:
				maze[0][0][2] = 0
			if position[0] != self.gridSize - 1:
				maze[self.mazeSize - 1][self.mazeSize - 1][3] = 0

	def create_exit(self):
		downright = random.randint(0, 1)
		positioning = [random.randint(0, 1), random.randint(0, self.gridSize - 1)]
		downright = [(self.gridSize - 1) * downright * (1 - positioning[0]), (self.gridSize - 1) * downright * positioning[0]]
		position = [positioning[0] * positioning[1] + downright[0], (1 - positioning[0]) * positioning[1] + downright[1]]
		self.grid[position[1]][position[0]] = define_Maze(self.mazeSize)
		self.cut_chunkWalls([position[0], position[1]])

		Maze = self.grid[position[1]][position[0]].maze
		potentialPositions = []

		if position[0] != 0 and position[1] == self.gridSize - 1:
			for box in range(0, self.mazeSize):
				if Maze[self.mazeSize - 1][box][0] + Maze[self.mazeSize - 1][box][1] + Maze[self.mazeSize - 1][box][2] + Maze[self.mazeSize - 1][box][3] >= 2:
					potentialPositions.append(box)
			exitPosition = random.choice(potentialPositions)
			Maze[self.mazeSize - 1][exitPosition][0] = 0
	
		if position[0] != self.gridSize - 1 and position[1] == 0:
			for box in range(0, self.mazeSize):
				if Maze[0][box][0] + Maze[0][box][1] + Maze[0][box][2] + Maze[0][box][3] >= 2:
					potentialPositions.append(box)
			exitPosition = random.choice(potentialPositions)
			Maze[0][exitPosition][1] = 0
		
		if position[0] == 0 and position[1] != self.gridSize - 1:
			for box in range(0, self.mazeSize):
				if Maze[box][0][0] + Maze[box][0][1] + Maze[box][0][2] + Maze[box][0][3] >= 2:
					potentialPositions.append(box)
			exitPosition = random.choice(potentialPositions)
			Maze[exitPosition][0][2] = 0
		
		if position[0] == self.gridSize - 1 and position[1] != 0:
			for box in range(0, self.mazeSize):
				if Maze[box][self.mazeSize - 1][0] + Maze[box][self.mazeSize - 1][1] + Maze[box][self.mazeSize - 1][2] + Maze[box][self.mazeSize - 1][3] >= 2:
					potentialPositions.append(box)
			exitPosition = random.choice(potentialPositions)
			Maze[exitPosition][self.mazeSize - 1][3] = 0
		
	def check_emptyChunks(self, position):
		for y in range(self.displayChunk - int(self.displayChunk / 2) - self.displayChunk, self.displayChunk - int(self.displayChunk / 2)):
			if position[1] + y < 0 or position[1] + y > self.gridSize - 1:
				continue
			if self.grid[position[1] + y][position[0]] == None:
				return [position[0], position[1] + y]
		for x in range(self.displayChunk - int(self.displayChunk / 2) - self.displayChunk, self.displayChunk - int(self.displayChunk / 2)):
			if position[0] + x < 0 or position[0] + x > self.gridSize - 1:
				continue
			if self.grid[position[1]][position[0] + x] == None:
				return [position[0] + x, position[1]]
		return True

	def update_chunks(self, position):
		goodChunks = self.check_emptyChunks(position)
		while goodChunks != True:
			self.grid[goodChunks[1]][goodChunks[0]] = define_Maze(self.mazeSize)
			self.cut_chunkWalls([goodChunks[0], goodChunks[1]])
			goodChunks = self.check_emptyChunks(position)

Grid = define_Grid(101)
