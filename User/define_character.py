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
		
		self.running = False
		self.maxStamina = 135
		self.staminaTime = 5
		self.staminaGain = 4
		self.stamina = self.maxStamina
		
		self.tired = False
		self.cooldown = 2
		self.timePassed = self.cooldown
		
		self.movement = [0, 0]
		self.maxVelocity = self.width / 5
		self.velocity = [0, 0]
		self.speedGain = 1 / 5
		self.stillFriction = .85
		self.movingFriction = .9
		
		self.runningmaxVelocity = self.maxVelocity * 1.5
		self.runningspeedGain = self.speedGain * 1.5
		self.tiredmaxVelocity = self.maxVelocity / 2
		self.tiredspeedGain = self.speedGain / 2
		
	def update_running(self):
		if self.stamina <= 0 and not self.tired:
			self.running = False
			self.stamina = 0
			self.tired = True
			self.timePassed = 0
		if not self.tired:
			if not self.running and self.stamina != self.maxStamina:
				self.stamina += self.maxStamina / self.staminaGain / User.FPS
			if self.stamina > self.maxStamina:
				self.stamina = self.maxStamina
		else:
			if self.timePassed <= self.cooldown:
				self.timePassed += 1 / User.FPS
			else:
				self.stamina += self.maxStamina / self.staminaGain / User.FPS
				self.tired = False
		if self.running and self.stamina != 0:
			self.stamina -= self.maxStamina / self.staminaTime / User.FPS
		self.color[0] = 195 - int(135 * (self.stamina / self.maxStamina))
		self.color[2] = 60 + int(135 * (self.stamina / self.maxStamina))
	
	def update_velocity(self):
		self.update_running()
		if self.running:
			self.velocity[0] += self.runningmaxVelocity * self.runningspeedGain * self.movement[0]
			self.velocity[1] += self.runningmaxVelocity * self.runningspeedGain * self.movement[1]
		elif self.tired:
			self.velocity[0] += self.tiredmaxVelocity * self.tiredspeedGain * self.movement[0]
			self.velocity[1] += self.tiredmaxVelocity * self.tiredspeedGain * self.movement[1]
		else:
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

		if self.running:
			if abs(self.velocity[0]) > self.runningmaxVelocity:
				self.velocity[0] *= self.stillFriction
			if abs(self.velocity[1]) > self.runningmaxVelocity:
				self.velocity[1] *= self.stillFriction
		elif self.tired:
			if abs(self.velocity[0]) > self.tiredmaxVelocity:
				self.velocity[0] *= self.stillFriction
			if abs(self.velocity[1]) > self.tiredmaxVelocity:
				self.velocity[0] *= self.stillFriction
		else:
			if abs(self.velocity[0]) > self.maxVelocity:
				self.velocity[0] *= self.stillFriction
			if abs(self.velocity[1]) > self.maxVelocity:
				self.velocity[1] *= self.stillFriction

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
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]
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
