import random, os, pickle
from User.define_user import User
from Grid.define_maze import define_Maze

class define_Grid:
	def __init__(self):	
		self.gridSize = 101
		self.mazeSize = 51
		self.boxSize = 1
		
		self.defultdisplaymazeSize = 9
		self.displaymazeSize = self.defultdisplaymazeSize
		self.displayChunk = int(self.displaymazeSize / self.mazeSize) + 1
		self.wallWidth = (9 / self.displaymazeSize) / 20

		self.grid = []
		for row in range(self.gridSize):
			self.grid.append([])
			for column in range(self.gridSize):
				self.grid[row].append(None)
		self.create_exit()

	def cut_chunkWalls(self, position):
		maze = self.grid[position[1]][position[0]].maze
		if position[1] != self.gridSize - 1:
			if self.grid[position[1] + 1][position[0]] != None:
				sideMaze = self.grid[position[1] + 1][position[0]].maze
				crossedWalls = [True, True]
				canCut = True
				holes = []
				for col in range(0, self.mazeSize):
					if col - 1 not in holes:
						canCut = True
					if maze[self.mazeSize - 1][col][2] == 1 and col != 0:
						crossedWalls[0] = True
					if sideMaze[0][col][2] == 1 and col != 0:
						crossedWalls[1] = True
					if canCut == True and False not in crossedWalls:
						if maze[self.mazeSize - 1][col][0] + maze[self.mazeSize - 1][col][1] + maze[self.mazeSize - 1][col][2] + maze[self.mazeSize - 1][col][3] < 2:
							continue
						if sideMaze[0][col][0] + sideMaze[0][col][1] + sideMaze[0][col][2] + sideMaze[0][col][3] < 2:
							continue
						if not random.randint(0, 1):
							continue
						holes.append(col)
						crossedWalls = [False, False]
						canCut = False
				if len(holes) == 0:
					hole = random.radnint(0, self.mazeSize)
					maze[self.mazeSize - 1][hole][0] = 0
					sideMaze[0][hole][1] = 0
				else:
					for hole in holes:
						maze[self.mazeSize - 1][hole][0] = 0
						sideMaze[0][hole][1] = 0

		if position[1] != 0:
			if self.grid[position[1] - 1][position[0]] != None:
				sideMaze = self.grid[position[1] - 1][position[0]].maze
				crossedWalls = [True, True]
				canCut = True
				holes = []
				for col in range(0, self.mazeSize):
					if col - 1 not in holes:
						canCut = True
					if maze[0][col][2] == 1 and col != 0:
						crossedWalls[0] = True
					if sideMaze[self.mazeSize - 1][col][2] == 1 and col != 0:
						crossedWalls[1] = True
					if canCut == True and False not in crossedWalls:
						if maze[0][col][0] + maze[0][col][1] + maze[0][col][2] + maze[0][col][3] < 2:
							continue
						if sideMaze[self.mazeSize - 1][col][0] + sideMaze[self.mazeSize - 1][col][1] + sideMaze[self.mazeSize - 1][col][2] + sideMaze[self.mazeSize - 1][col][3] < 2:
							continue
						if not random.randint(0, 1):
							continue
						holes.append(col)
						crossedWalls = [False, False]
						canCut = False
				if len(holes) == 0:
					hole = random.radnint(0, self.mazeSize)
					maze[0][hole][1] = 0
					sideMaze[self.mazeSize - 1][hole][0] = 0
				else:
					for hole in holes:
						maze[0][hole][1] = 0
						sideMaze[self.mazeSize - 1][hole][0] = 0

		if position[0] != 0:
			if self.grid[position[1]][position[0] - 1] != None:
				sideMaze = self.grid[position[1]][position[0] - 1].maze
				crossedWalls = [True, True]
				canCut = True
				holes = []
				for row in range(0, self.mazeSize):
					if row - 1 not in holes:
						canCut = True
					if maze[row][0][1] == 1 and row != 0:
						crossedWalls[0] = True
					if sideMaze[row][self.mazeSize - 1][1] == 1 and row != 0:
						crossedWalls[1] = True
					if canCut == True and False not in crossedWalls:
						if maze[row][0][0] + maze[row][0][1] + maze[row][0][2] + maze[row][0][3] < 2:
							continue
						if sideMaze[row][self.mazeSize - 1][0] + sideMaze[row][self.mazeSize - 1][1] + sideMaze[row][self.mazeSize - 1][2] + sideMaze[row][self.mazeSize - 1][3] < 2:
							continue
						if not random.randint(0, 2):
							continue
						holes.append(row)
						crossedWalls = [False, False]
						canCut = False
				if len(holes) == 0:
					hole = random.radnint(0, self.mazeSize)
					maze[hole][0][2] = 0
					sideMaze[hole][self.mazeSize - 1][3] = 0
				else:
					for hole in holes:
						maze[hole][0][2] = 0
						sideMaze[hole][self.mazeSize - 1][3] = 0
		
		if position[0] != self.gridSize - 1:
			if self.grid[position[1]][position[0] + 1] != None:
				sideMaze = self.grid[position[1]][position[0] + 1].maze
				crossedWalls = [True, True]
				canCut = True
				holes = []
				for row in range(0, self.mazeSize):
					if row - 1 not in holes:
						canCut = True
					if maze[row][self.mazeSize - 1][1] == 1 and row != 0:
						crossedWalls[0] = True
					if sideMaze[row][0][1] == 1 and row != 0:
						crossedWalls[1] = True
					if canCut == True and False not in crossedWalls:
						if maze[row][self.mazeSize - 1][0] + maze[row][self.mazeSize - 1][1] + maze[row][self.mazeSize - 1][2] + maze[row][self.mazeSize - 1][3] < 2:
							continue
						if sideMaze[row][0][0] + sideMaze[row][0][1] + sideMaze[row][0][2] + sideMaze[row][0][3] < 2:
							continue
						if not random.randint(0, 2):
							continue
						holes.append(row)
						crossedWalls = [False, False]
						canCut = False
				if len(holes) == 0:
					hole = random.radnint(0, self.mazeSize)
					maze[hole][self.mazeSize - 1][3] = 0
					sideMaze[hole][0][2] = 0
				else:
					for hole in holes:
						maze[hole][self.mazeSize - 1][3] = 0
						sideMaze[hole][0][2] = 0

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
		for y in range(-1, 2):
			if position[1] + y < 0 or position[1] + y > self.gridSize - 1:
				continue
			if self.grid[position[1] + y][position[0]] == None:
				return [position[0], position[1] + y]
		for x in range(-1, 2):
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

Grid = define_Grid()
