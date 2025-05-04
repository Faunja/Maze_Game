import os, pickle
from User.define_user import User
from Grid.define_grid import Grid

class define_Character():
	def __init__(self):
		self.completedMaze = False

		self.color = (60, 60, 195)
		self.width = 1 / 4
		self.outline = 4 / 5

		self.position = [0, 0]
		self.startgridPosition = [int(Grid.gridSize / 2), int(Grid.gridSize / 2)]
		self.gridPosition = self.startgridPosition
		self.mazePosition = [int(Grid.mazeSize / 2), int(Grid.mazeSize / 2)]

		self.movement = [0, 0]
		self.maxVelocity = self.width / 5
		self.velocity = [0, 0]
		self.speedGain = 1 / 5
		self.stillFriction = .8
		self.movingFriction = .9

		self.differenceLimit = [Grid.displaymazeSize / 4, Grid.displaymazeSize / 4]
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
		if round(self.cameraPosition[0], int(Grid.mazeSize / 3)) == round(self.position[0], int(Grid.mazeSize / 3)) and round(self.cameraPosition[1], int(Grid.mazeSize / 3)) == round(self.position[1], int(Grid.mazeSize / 3)):
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

	def update_gridPosition(self):
		self.gridPosition = [round(Grid.gridSize / 2) + round(self.position[0] / Grid.mazeSize), round(Grid.gridSize / 2) + round(self.position[1] / Grid.mazeSize)]
		if self.gridPosition[0] <= -1:
			self.completedMaze = True
			return
		if self.gridPosition[0] >= Grid.gridSize:
			self.completedMaze = True
			return
		if self.gridPosition[1] <= -1:
			self.completedMaze = True
			return
		if self.gridPosition[1] >= Grid.gridSize:
			self.completedMaze = True
			return
		currentgridPosition = [self.gridPosition[0] - self.startgridPosition[0], self.gridPosition[1] - self.startgridPosition[1]]
		xmazePosition = int(Grid.mazeSize / 2) + round(self.position[0] / Grid.boxSize) - currentgridPosition[0] * Grid.mazeSize
		ymazePosition = int(Grid.mazeSize / 2) + round(self.position[1] / Grid.boxSize) - currentgridPosition[1] * Grid.mazeSize
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
	
	def move_character(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]
		self.update_camera()
		self.update_velocity()
		if self.completedMaze == False:
			self.update_gridPosition()
			self.hit_mazeWall()

if os.path.exists('Save_data/Character.pkl'):
	with open('Save_data/Character.pkl', 'rb') as file:
		Character = pickle.load(file)
else:
	Character = define_Character()
