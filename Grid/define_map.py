import pygame, os, pickle
from pygame.locals import *
from User.define_user import User
from Display.define_display import Display
from User.define_character import Character
from Grid.define_grid import Grid

class define_Map:
	def load_map(self):
		with open('Save_data/Map.pkl', 'rb') as file:
			reference = pickle.load(file)
			self.oldPositions = reference.oldPositions
			self.storedPositions = reference.storedPositions
	
	def __init__(self):
		self.oldPositions = []
		self.storedPositions = []
		for row in range(Grid.gridSize):
			self.storedPositions.append([])
			for column in range(Grid.gridSize):
				self.storedPositions[row].append([])
		self.currentPositions = [[Character.gridPosition.copy(), Character.mazePosition.copy()]]
		
		self.displayMap = False
		self.grabbedMap = False
		self.oldmousePosition = None
		self.mapPosition = Character.cameraPosition.copy()
		self.gridPosition = Character.gridPosition.copy()

		self.movement = [0, 0]
		self.mapVelocity = [False, False]
		self.maxVelocity = Character.width / (Grid.displaymazeSize / Grid.mapdisplaymazeSize * 5)
		self.velocity = [0, 0]
		self.speedGain = 1 / 5
		self.stillFriction = .8
		self.movingFriction = .9
		
		if os.path.exists('Save_data/Map.pkl'):
			self.load_map()

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

	def update_velocity(self):
		self.velocity[0] += self.maxVelocity * self.speedGain * self.movement[0]
		self.velocity[1] += self.maxVelocity * self.speedGain * self.movement[1]
		if self.movement[0] != 0 or self.mapVelocity[0] == True:
			self.velocity[0] *= self.movingFriction
		else:
			self.velocity[0] *= self.stillFriction
		if self.movement[1] != 0 or self.mapVelocity[1] == True:
			self.velocity[1] *= self.movingFriction
		else:
			self.velocity[1] *= self.stillFriction
		if abs(self.velocity[0]) > self.maxVelocity:
			if self.mapVelocity[0] == False:
				self.velocity[0] = abs(self.velocity[0]) / self.velocity[0] * self.maxVelocity
		else:
			self.mapVelocity[0] = False
		if abs(self.velocity[1]) > self.maxVelocity:
			if self.mapVelocity[1] == False:
				self.velocity[1] = abs(self.velocity[1]) / self.velocity[1] * self.maxVelocity
		else:
			self.mapVelocity[1] = False
	
	def update_gridPosition(self):
		self.gridPosition = [round(Grid.gridSize / 2) + round(self.mapPosition[0] / Grid.mazeSize), round(Grid.gridSize / 2) + round(self.mapPosition[1] / Grid.mazeSize)]
		if self.gridPosition[0] <= -1:
			self.gridPosition[0] = 0
		if self.gridPosition[0] >= Grid.gridSize:
			self.gridPosition[0] = Grid.gridSize - 1
		if self.gridPosition[1] <= -1:
			self.gridPosition[1] = 0
		if self.gridPosition[1] >= Grid.gridSize:
			self.gridPosition[1] = Grid.gridSize - 1

	def update_position(self):
		if self.grabbedMap == False:
			self.oldmousePosition = None
			self.mapPosition[0] += self.velocity[0]
			self.mapPosition[1] += self.velocity[1]
			self.update_velocity()
			return
		mousePosition = pygame.mouse.get_pos()
		if self.oldmousePosition == None:
			self.oldmousePosition = mousePosition
			return
		self.mapPosition[0] -= (mousePosition[0] - self.oldmousePosition[0]) / Display.maptileSize
		self.mapPosition[1] -= (mousePosition[1] - self.oldmousePosition[1]) / Display.maptileSize
		self.velocity[0] = -(mousePosition[0] - self.oldmousePosition[0]) / Display.maptileSize
		self.velocity[1] = -(mousePosition[1] - self.oldmousePosition[1]) / Display.maptileSize
		if abs(self.velocity[0]) > self.maxVelocity:
			self.mapVelocity[0] = True
		if abs(self.velocity[1]) > self.maxVelocity:
			self.mapVelocity[1] = True
		self.oldmousePosition = mousePosition
		if mousePosition[0] < 0 or mousePosition[0] > Display.DisplayWidth or mousePosition[1] < 0 or mousePosition[1] > Display.DisplayWidth:
			self.grabbedMap = False

	def update_mapSize(self, direction):
		Grid.mapdisplaymazeSize += 2 * direction
		if Grid.mapdisplaymazeSize < Grid.displaymazeSize:
			Grid.mapdisplaymazeSize = Grid.displaymazeSize
		if Grid.mapdisplaymazeSize > Grid.defualtmapSize * 3:
			Grid.mapdisplaymazeSize = Grid.defualtmapSize * 3

		if Grid.mapdisplaymazeSize < Grid.mazeSize:
			Grid.mapdisplayChunk = 3
		else:
			Grid.mapdisplayChunk = int(Grid.mapdisplaymazeSize / Grid.mazeSize * 3)
			if Grid.mapdisplayChunk % 2 == 0:
				Grid.mapdisplayChunk += 1
		Display.maptileSize = Display.DisplayHeight / Grid.mapdisplaymazeSize

	def update_map(self):
		self.update_oldPositions()
		self.update_currentPosition()
		if self.displayMap == False:
			self.mapPosition = Character.cameraPosition.copy()
			self.gridPosition = Character.gridPosition.copy()
		else:
			self.update_position()
			self.update_gridPosition()

Map = define_Map()
