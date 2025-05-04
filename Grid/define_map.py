from User.define_user import User
from User.define_character import Character
from Grid.define_grid import Grid

class define_Map:
	def __init__(self):
		self.currentPositions = [[Character.gridPosition, Character.mazePosition]]
		self.oldPositions = []
		self.storedPositions = []
		for row in range(Grid.gridSize):
			self.storedPositions.append([])
			for column in range(Grid.gridSize):
				self.storedPositions[row].append([])
	
	def update_oldPositions(self):
		for position in self.currentPositions:
			if position[1] in self.storedPositions[position[0][1]][position[0][0]]:
				continue
			self.storedPositions[position[0][1]][position[0][0]].append(position[1])

	def update_currentPosition(self):
		self.currentPositions = []
		self.currentPositions.append([Character.gridPosition, Character.mazePosition])
		checkNegative = [[True, 0, 0], [True, 0, 0]]
		checkPositive = [[True, 0, 0], [True, 0, 0]]
		while checkNegative[0][0]:
			checkNegative[0][2] -= 1
			if checkNegative[0][2] + Character.mazePosition[0] < 0:
				checkNegative[0][2] += Grid.mazeSize
				checkNegative[0][1] -= 1
			if Character.gridPosition[0] + checkNegative[0][1] < 0:
				break
			Maze = Grid.grid[Character.gridPosition[1]][Character.gridPosition[0] + checkNegative[0][1]]
			if Maze == None:
				break
			mazeBox = Maze.maze[Character.mazePosition[1]][Character.mazePosition[0] + checkNegative[0][2]]
			if mazeBox[3] == 1:
				checkNegative[0][0] = False
				break
			self.currentPositions.append([[Character.gridPosition[0] + checkNegative[0][1], Character.gridPosition[1]], [Character.mazePosition[0] + checkNegative[0][2], Character.mazePosition[1]]])

		while checkPositive[0][0]:
			checkPositive[0][2] += 1
			if checkPositive[0][2] + Character.mazePosition[0] == Grid.mazeSize:
				checkPositive[0][2] -= Grid.mazeSize
				checkPositive[0][1] += 1
			if Character.gridPosition[0] + checkPositive[0][1] > Grid.gridSize - 1:
				break
			Maze = Grid.grid[Character.gridPosition[1]][Character.gridPosition[0] + checkPositive[0][1]]
			if Maze == None:
				break
			mazeBox = Maze.maze[Character.mazePosition[1]][Character.mazePosition[0] + checkPositive[0][2]]
			if mazeBox[2] == 1:
				checkPositive[0][0] = False
				break
			self.currentPositions.append([[Character.gridPosition[0] + checkPositive[0][1], Character.gridPosition[1]], [Character.mazePosition[0] + checkPositive[0][2], Character.mazePosition[1]]])
		
		while checkNegative[1][0]:
			checkNegative[1][2] -= 1
			if checkNegative[1][2] + Character.mazePosition[1] < 0:
				checkNegative[1][2] += Grid.mazeSize
				checkNegative[1][1] -= 1
			if Character.gridPosition[1] + checkNegative[1][1] < 0:
				break
			Maze = Grid.grid[Character.gridPosition[1] + checkNegative[1][1]][Character.gridPosition[0]]
			if Maze == None:
				break
			mazeBox = Maze.maze[Character.mazePosition[1] + checkNegative[1][2]][Character.mazePosition[0]]
			if mazeBox[0] == 1:
				checkNegative[1][0] = False
				break
			self.currentPositions.append([[Character.gridPosition[0], Character.gridPosition[1] + checkNegative[1][1]], [Character.mazePosition[0], Character.mazePosition[1] + checkNegative[1][2]]])
		
		while checkPositive[1][0]:
			checkPositive[1][2] += 1
			if checkPositive[1][2] + Character.mazePosition[1] == Grid.mazeSize:
				checkPositive[1][2] -= Grid.mazeSize
				checkPositive[1][1] += 1
			if Character.gridPosition[1] + checkPositive[1][1] > Grid.gridSize - 1:
				break
			Maze = Grid.grid[Character.gridPosition[1] + checkPositive[1][1]][Character.gridPosition[0]]
			if Maze == None:
				break
			mazeBox = Maze.maze[Character.mazePosition[1] + checkPositive[1][2]][Character.mazePosition[0]]
			if mazeBox[1] == 1:
				checkPositive[1][0] = False
				break
			self.currentPositions.append([[Character.gridPosition[0], Character.gridPosition[1] + checkPositive[1][1]], [Character.mazePosition[0], Character.mazePosition[1] + checkPositive[1][2]]])
	
	def update_map(self):
		self.update_oldPositions()
		self.update_currentPosition()

Map = define_Map()