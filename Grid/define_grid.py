import pygame, random, copy
from pygame.locals import *
from User.define_user import User
from Display.define_display import Display
from Grid.define_maze import define_Maze

class define_Grid:
	def __init__(self, gridSize):
		self.mazeSize = 9
		self.boxSize = round(Display.DisplayHeight / self.mazeSize)
		self.wallWidth = round(Display.DisplayHeight / 172)
		if self.wallWidth < 1:
			self.allWidth = 1
		
		self.gridSize = gridSize
		self.grid = []
		for row in range(self.gridSize):
			self.grid.append([])
			for column in range(self.gridSize):
				self.grid[row].append(None)

	def check_emptyChunks(self, position):
		for x in range(-1, 2):
			for y in range(-1, 2):
				if self.grid[position[1] + y][position[0] + x] == None:
					return [position[0] + x, position[1] + y]
		return True

	def check_sideChunks(self, position):
		sideChunks = []
		for y in range(-1, 2):
			for x in range(-1, 2):
				if abs(y) == abs(x):
					continue
				if self.grid[position[1] + y][position[0] + x] != None:
					sideChunks.append([position[0] + x, position[1] + y])
		return sideChunks

	def cut_chunkWalls(self, position):
		maze = self.grid[position[1]][position[0]].maze
		if position[0] % 2 == position[1] % 2:
			maze[self.mazeSize - 1][self.mazeSize - 1][0] = 0
			maze[0][0][1] = 0
			maze[self.mazeSize - 1][0][2] = 0
			maze[0][self.mazeSize - 1][3] = 0
		else:
			maze[self.mazeSize - 1][0][0] = 0
			maze[0][self.mazeSize - 1][1] = 0
			maze[0][0][2] = 0
			maze[self.mazeSize - 1][self.mazeSize - 1][3] = 0

	def update_chunks(self, position):
		goodChunks = self.check_emptyChunks(position)
		while goodChunks != True:
			self.grid[goodChunks[1]][goodChunks[0]] = define_Maze(self.mazeSize)
			sideChunks = self.check_sideChunks([goodChunks[0], goodChunks[1]])
			self.cut_chunkWalls([goodChunks[0], goodChunks[1]])
			goodChunks = self.check_emptyChunks(position)

Grid = define_Grid(101)
