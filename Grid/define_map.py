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
			self.cameraPosition = reference.position.copy()
	
	def __init__(self):
		self.oldPositions = []
		self.storedPositions = []
		for row in range(Grid.gridSize):
			self.storedPositions.append([])
			for column in range(Grid.gridSize):
				self.storedPositions[row].append([])
		self.currentPositions = [[Character.gridPosition.copy(), Character.mazePosition.copy()]]
		
		self.centeredMap = True
		self.cameraMoving = False
		self.grabbedMap = False
		self.oldmousePosition = None
		
		self.cameraPosition = [0, 0]
		self.differenceLimit = [Grid.displaymazeSize / 4, Grid.displaymazeSize / 4]
		self.cameraVelocity = 1 / 20
		self.velocity = [0, 0]
		self.friction = .8
		
		self.displaygridPosition = Character.gridPosition.copy()
		
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
	
	def adjust_camera(self):
		if self.cameraPosition[0] > Character.position[0] + self.differenceLimit[0] or self.cameraPosition[0] < Character.position[0] - self.differenceLimit[0]:
			self.cameraMoving = True
		if self.cameraPosition[1] > Character.position[1] + self.differenceLimit[1] or self.cameraPosition[1] < Character.position[1] - self.differenceLimit[1]:
			self.cameraMoving = True
		if self.cameraMoving == True:
			self.cameraPosition[0] += (Character.position[0] - self.cameraPosition[0]) * self.cameraVelocity
			self.cameraPosition[1] += (Character.position[1] - self.cameraPosition[1]) * self.cameraVelocity
		if round(self.cameraPosition[0], int(Grid.mazeSize / 3)) == round(Character.position[0], int(Grid.mazeSize / 3)) and round(self.cameraPosition[1], int(Grid.mazeSize / 3)) == round(Character.position[1], int(Grid.mazeSize / 3)):
			self.cameraMoving = False
	
	def move_camera(self):
		if self.grabbedMap == False:
			self.oldmousePosition = None
			self.cameraPosition[0] += self.velocity[0]
			self.cameraPosition[1] += self.velocity[1]
			self.velocity[0] *= self.friction
			self.velocity[1] *= self.friction
			return
		mousePosition = pygame.mouse.get_pos()
		if self.oldmousePosition == None:
			self.oldmousePosition = mousePosition
			return
		self.cameraPosition[0] -= (mousePosition[0] - self.oldmousePosition[0]) / Display.tileSize
		self.cameraPosition[1] -= (mousePosition[1] - self.oldmousePosition[1]) / Display.tileSize
		self.velocity[0] = -(mousePosition[0] - self.oldmousePosition[0]) / Display.tileSize
		self.velocity[1] = -(mousePosition[1] - self.oldmousePosition[1]) / Display.tileSize
		self.oldmousePosition = mousePosition
		if mousePosition[0] < 0 or mousePosition[0] > Display.DisplayWidth or mousePosition[1] < 0 or mousePosition[1] > Display.DisplayWidth:
			self.grabbedMap = False

	def update_mapSize(self, direction):
		Grid.displaymazeSize += 2 * direction
		if Grid.displaymazeSize < Grid.defultdisplaymazeSize:
			Grid.displaymazeSize = Grid.defultdisplaymazeSize
		if Grid.displaymazeSize > Grid.defultdisplaymazeSize * 3:
			Grid.displaymazeSize = Grid.defultdisplaymazeSize * 3

		if Grid.displaymazeSize < Grid.mazeSize:
			Grid.displayChunk = 3
		else:
			Grid.displayChunk = int(Grid.displaymazeSize / Grid.mazeSize * 3)
			if Grid.displayChunk % 2 == 0:
				Grid.displayChunk += 1
		Display.tileSize = Display.DisplayHeight / Grid.displaymazeSize

	def update_map(self):
		if Character.completedMaze:
			return
		self.update_oldPositions()
		self.update_currentPosition()
		self.displaygridPosition = [round(Grid.gridSize / 2) + round(self.cameraPosition[0] / Grid.mazeSize), round(Grid.gridSize / 2) + round(self.cameraPosition[1] / Grid.mazeSize)]
		if self.centeredMap:
			self.adjust_camera()
		else:
			self.move_camera()
		

Map = define_Map()
