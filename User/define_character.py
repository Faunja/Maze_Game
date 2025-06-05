import os, pickle, random
from User.define_user import User
from Grid.define_grid import Grid

class define_Character():
	def __init__(self):
		self.timeSpent = [0, 0, 0]
		self.completedMaze = False
		
		self.color = [60, 60, 195]
		self.width = 1 / 4
		self.outline = 4 / 5
		self.position = [0, 0]
		self.startgridPosition = [int(Grid.gridSize / 2), int(Grid.gridSize / 2)]
		self.gridPosition = self.startgridPosition
		self.mazePosition = [int(Grid.mazeSize / 2), int(Grid.mazeSize / 2)]
		
		self.maxVelocity = self.width / 5
		self.velocity = [0, 0]
		self.speedGain = 1 / 80
		self.stillFriction = 128
		self.movingFriction = 135
		
		self.direction = [0, 0]
		self.movements = {"walking" : 1, "running" : 1.5, "tired" : .5}
		self.moving = "walking"
		self.stamina = [135, 135]
		self.staminaTime = 5
		self.staminaGain = 4
		self.cooldown = [32, 32]

	def update_running(self):
		if self.stamina[1] <= 0 and self.moving != "tired":
			self.stamina[1] = 0
			self.cooldown[1] = 0
		if self.moving != "tired":
			if self.moving != "running" and self.stamina[1] != self.stamina[0]:
				self.stamina[1] += self.stamina[0] / self.staminaGain / User.actualFPS
			if self.stamina[1] > self.stamina[0]:
				self.stamina[1] = self.stamina[0]
		else:
			if self.cooldown[1] <= self.cooldown[0]:
				self.cooldown[1] += 1 / 16 * User.deltaTime / User.actualFPS
			else:
				self.stamina[1] += self.stamina[0] / self.staminaGain / User.actualFPS
		if self.moving == "running" and self.stamina[1] != 0:
			self.stamina[1] -= self.stamina[0] / self.staminaTime / User.actualFPS
		self.color[0] = 195 - int(135 * (self.stamina[1] / self.stamina[0]))
		self.color[2] = 60 + int(135 * (self.stamina[1] / self.stamina[0]))
	
	def update_velocity(self):
		self.update_running()
		self.velocity[0] += (self.maxVelocity * self.movements[self.moving]) * (self.speedGain * User.deltaTime * self.movements[self.moving]) * self.direction[0]
		self.velocity[1] += (self.maxVelocity * self.movements[self.moving]) * (self.speedGain * User.deltaTime * self.movements[self.moving]) * self.direction[1]

		if self.direction[0] != 0:
			self.velocity[0] -= self.velocity[0] / self.movingFriction * User.deltaTime
		else:
			self.velocity[0] -= self.velocity[0] / self.stillFriction * User.deltaTime
		if self.direction[1] != 0:
			self.velocity[1] -= self.velocity[1] / self.movingFriction * User.deltaTime
		else:
			self.velocity[1] -= self.velocity[1] / self.stillFriction * User.deltaTime

		if abs(self.velocity[0]) > self.maxVelocity * self.movements[self.moving]:
			self.velocity[0] = self.maxVelocity * self.movements[self.moving] * (abs(self.velocity[0]) / self.velocity[0])
		if abs(self.velocity[1]) > self.maxVelocity * self.movements[self.moving]:
			self.velocity[1] = self.maxVelocity * self.movements[self.moving] * (abs(self.velocity[1]) / self.velocity[1])

	def hit_mazeWall(self):
		if self.completedMaze:
			return
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
		if xmazePosition != self.mazePosition[0] and ymazePosition != self.mazePosition[1]:
			if abs(self.velocity[0]) > abs(self.velocity[1]):
				ymazePosition = self.mazePosition[1]
			elif abs(self.velocity[1]) > abs(self.velocity[0]):
				xmazePosition = self.mazePosition[0]
			else:
				direction = random.randint(0, 1)
				xmazePosition += (self.mazePosition[0] - xmazePosition) * direction
				ymazePosition += (self.mazePosition[1] - ymazePosition) * (1 - direction)
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
	
	def update_character(self):
		self.position[0] += self.velocity[0] / 16 * User.deltaTime
		self.position[1] += self.velocity[1] / 16 * User.deltaTime
		self.update_velocity()
		if self.completedMaze == False:
			self.update_gridPosition()
			self.hit_mazeWall()
			self.timeSpent[0] += 1 / User.FPS
			if self.timeSpent[0] >= 60:
				self.timeSpent[1] += 1
				self.timeSpent[0] -= 60
				if self.timeSpent[1] >= 60:
					self.timeSpent[2] += 1
					self.timeSpent[1] -= 60

Character = define_Character()
