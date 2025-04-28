import pygame, time, copy
from pygame.locals import *
from User.define_user import User
from User.define_display import Display
from Grid.define_grid import Grid

class define_Character():
	def __init__(self):
		self.color = (60, 60, 195)
		self.width = Grid.boxSize / 4
		self.outline = 4 / 5

		self.position = [0, 0]
		self.startgridPosition = [round(Grid.gridSize / 2), round(Grid.gridSize / 2)]
		self.gridPosition = self.startgridPosition
		self.mazePosition = [round(Grid.mazeSize / 2), round(Grid.mazeSize / 2)]
		self.currentPositions = [[self.gridPosition, self.mazePosition]]
		self.oldPositions = []
		self.storedPositions = []
		for row in range(Grid.gridSize):
			self.storedPositions.append([])
			for column in range(Grid.gridSize):
				self.storedPositions[row].append([])

		self.movement = [0, 0]
		self.maxVelocity = self.width / 5
		self.velocity = [0, 0]
		self.speedGain = 1 / 5
		self.stillFriction = .8
		self.movingFriction = .9

		self.differenceLimit = [Display.DisplayWidth / 4, Display.DisplayHeight / 4]
		self.cameraMoving = False
		self.cameraPosition = [0, 0]
		self.cameraVelocity = 1 / 20

	def update_velocity(self):
		self.velocity[0] += self.maxVelocity * self.speedGain * self.movement[0]
		self.velocity[1] += self.maxVelocity * self.speedGain * self.movement[1]
		if self.movement[0] != 0:
			self.velocity[0] *= self.movingFriction
		else:
			self.velocity[0] *= self.stillFriction
		if self.movement[1] != 0:
			self.velocity[1] *= self.movingFriction
		else:
			self.velocity[1] *= self.stillFriction
		if abs(self.velocity[0]) > self.maxVelocity:
			self.velocity[0] = abs(self.velocity[0]) / self.velocity[0] * self.maxVelocity
		if abs(self.velocity[1]) > self.maxVelocity:
			self.velocity[1] = abs(self.velocity[1]) / self.velocity[1] * self.maxVelocity

	def update_camera(self):
		if self.cameraPosition[0] > self.position[0] + self.differenceLimit[0] or self.cameraPosition[0] < self.position[0] - self.differenceLimit[0]:
			self.cameraMoving = True
		if self.cameraPosition[1] > self.position[1] + self.differenceLimit[1] or self.cameraPosition[1] < self.position[1] - self.differenceLimit[1]:
			self.cameraMoving = True
		if self.cameraMoving == True:
			self.cameraPosition[0] += (self.position[0] - self.cameraPosition[0]) * self.cameraVelocity
			self.cameraPosition[1] += (self.position[1] - self.cameraPosition[1]) * self.cameraVelocity
		if round(self.cameraPosition[0]) == round(self.position[0]) and round(self.cameraPosition[1]) == round(self.position[1]):
			self.cameraMoving = False

	def hit_mazeWall(self):
		currentgridPosition = [self.startgridPosition[0] - self.gridPosition[0], self.startgridPosition[1] - self.gridPosition[1]]
		xminPosition = (self.mazePosition[0] - Grid.mazeSize / 2) * Grid.boxSize + self.width / 2 - currentgridPosition[0] * Grid.mazeSize * Grid.boxSize
		yminPosition = (self.mazePosition[1] - Grid.mazeSize / 2) * Grid.boxSize + self.width / 2 - currentgridPosition[1] * Grid.mazeSize * Grid.boxSize
		minPosition = [xminPosition, yminPosition]

		xmaxPosition = (self.mazePosition[0] + 1 - Grid.mazeSize / 2) * Grid.boxSize - self.width / 2 - currentgridPosition[0] * Grid.mazeSize * Grid.boxSize
		ymaxPosition = (self.mazePosition[1] + 1 - Grid.mazeSize / 2) * Grid.boxSize - self.width / 2 - currentgridPosition[1] * Grid.mazeSize * Grid.boxSize
		maxPosition = [xmaxPosition, ymaxPosition]

		Maze = Grid.grid[self.gridPosition[1]][self.gridPosition[0]]
		mazeBox = Maze.maze[self.mazePosition[1]][self.mazePosition[0]]
		
		if self.position[1] > maxPosition[1] and mazeBox[0] == 1:
			self.position[1] = maxPosition[1]
			self.velocity[1] = 0
		if self.position[1] < minPosition[1] and mazeBox[1] == 1:
			self.position[1] = minPosition[1]
			self.velocity[1] = 0
		if self.position[0] < minPosition[0] and mazeBox[2] == 1:
			self.position[0] = minPosition[0]
			self.velocity[0] = 0
		if self.position[0] > maxPosition[0] and mazeBox[3] == 1:
			self.position[0] = maxPosition[0]
			self.velocity[0] = 0

	def update_oldPositions(self):
		for position in self.currentPositions:
			if position[1] in self.storedPositions[position[0][1]][position[0][0]]:
				continue
			self.storedPositions[position[0][1]][position[0][0]].append(position[1])

	def update_currentPosition(self):
		self.currentPositions = []
		self.currentPositions.append([self.gridPosition, self.mazePosition])
		checkNegative = [[True, 0, 0], [True, 0, 0]]
		checkPositive = [[True, 0, 0], [True, 0, 0]]
		while checkNegative[0][0]:
			checkNegative[0][2] -= 1
			if checkNegative[0][2] + self.mazePosition[0] < 0:
				checkNegative[0][2] += Grid.mazeSize
				checkNegative[0][1] -= 1
			Maze = Grid.grid[self.gridPosition[1]][self.gridPosition[0] + checkNegative[0][1]]
			if Maze == None:
				break
			mazeBox = Maze.maze[self.mazePosition[1]][self.mazePosition[0] + checkNegative[0][2]]
			if mazeBox[3] == 1:
				checkNegative[0][0] = False
				break
			self.currentPositions.append([[self.gridPosition[0] + checkNegative[0][1], self.gridPosition[1]], [self.mazePosition[0] + checkNegative[0][2], self.mazePosition[1]]])

		while checkPositive[0][0]:
			checkPositive[0][2] += 1
			if checkPositive[0][2] + self.mazePosition[0] == Grid.mazeSize:
				checkPositive[0][2] -= Grid.mazeSize
				checkPositive[0][1] += 1
			Maze = Grid.grid[self.gridPosition[1]][self.gridPosition[0] + checkPositive[0][1]]
			mazeBox = Maze.maze[self.mazePosition[1]][self.mazePosition[0] + checkPositive[0][2]]
			if Maze == None:
				break
			if mazeBox[2] == 1:
				checkPositive[0][0] = False
				break
			self.currentPositions.append([[self.gridPosition[0] + checkPositive[0][1], self.gridPosition[1]], [self.mazePosition[0] + checkPositive[0][2], self.mazePosition[1]]])
		
		while checkNegative[1][0]:
			checkNegative[1][2] -= 1
			if checkNegative[1][2] + self.mazePosition[1] < 0:
				checkNegative[1][2] += Grid.mazeSize
				checkNegative[1][1] -= 1
			Maze = Grid.grid[self.gridPosition[1] + checkNegative[1][1]][self.gridPosition[0]]
			if Maze == None:
				break
			mazeBox = Maze.maze[self.mazePosition[1] + checkNegative[1][2]][self.mazePosition[0]]
			if mazeBox[0] == 1:
				checkNegative[1][0] = False
				break
			self.currentPositions.append([[self.gridPosition[0], self.gridPosition[1] + checkNegative[1][1]], [self.mazePosition[0], self.mazePosition[1] + checkNegative[1][2]]])
		
		while checkPositive[1][0]:
			checkPositive[1][2] += 1
			if checkPositive[1][2] + self.mazePosition[1] == Grid.mazeSize:
				checkPositive[1][2] -= Grid.mazeSize
				checkPositive[1][1] += 1
			Maze = Grid.grid[self.gridPosition[1] + checkPositive[1][1]][self.gridPosition[0]]
			if Maze == None:
				break
			mazeBox = Maze.maze[self.mazePosition[1] + checkPositive[1][2]][self.mazePosition[0]]
			if mazeBox[1] == 1:
				checkPositive[1][0] = False
				break
			self.currentPositions.append([[self.gridPosition[0], self.gridPosition[1] + checkPositive[1][1]], [self.mazePosition[0], self.mazePosition[1] + checkPositive[1][2]]])

	def update_gridPosition(self):
		self.gridPosition = [round(Grid.gridSize / 2) + round(self.position[0] / Display.DisplayWidth), round(Grid.gridSize / 2) + round(self.position[1] / Display.DisplayHeight)]
		currentgridPosition = [self.gridPosition[0] - self.startgridPosition[0], self.gridPosition[1] - self.startgridPosition[1]]
		xmazePosition = round(Grid.mazeSize / 2) + round(self.position[0] / Grid.boxSize) - currentgridPosition[0] * Grid.mazeSize
		ymazePosition = round(Grid.mazeSize / 2) + round(self.position[1] / Grid.boxSize) - currentgridPosition[1] * Grid.mazeSize
		self.mazePosition = [xmazePosition, ymazePosition]
		if self.mazePosition[0] <= -1:
			self.mazePosition[0] = 0
		if self.mazePosition[0] >= Grid.mazeSize:
			self.mazePosition[0] = Grid.mazeSize - 1
		if self.mazePosition[1] <= -1:
			self.mazePosition[1] = 0
		if self.mazePosition[1] >= Grid.mazeSize:
			self.mazePosition[1] = Grid.mazeSize - 1
		Grid.update_chunks(self.gridPosition)
		self.update_oldPositions()
		self.update_currentPosition()

	def move_character(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]
		self.update_camera()
		self.update_velocity()
		self.update_gridPosition()
		self.hit_mazeWall()

Character = define_Character()