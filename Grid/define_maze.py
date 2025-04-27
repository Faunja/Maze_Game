import pygame, random, copy
from pygame.locals import *
from User.define_user import User

class define_Maze:
	def check_position(self, checkedPosition, prePositions):
		for prePosition in prePositions:
			if checkedPosition == prePosition:
				return True
		if checkedPosition[0] == len(self.maze) or checkedPosition[0] < 0:
			return True
		if checkedPosition[1] == len(self.maze) or checkedPosition[1] < 0:
			return True
		return False

	def check_closedBox(self):
		for row in self.maze:
			for column in row:
				if column[0] == 1 and column[1] == 1 and column[2] == 1 and column[3] == 1:
					return True
		return False

	def create_maze(self, mazeSize):
		self.maze = []
		for row in range(mazeSize):
			self.maze.append([])
			for column in range(mazeSize):
				self.maze[row].append([1, 1, 1, 1])
		
		oldPositions = []
		position = [0, 0]
		insertPosition = 0

		closedBox = self.check_closedBox()

		while closedBox:
			canMove = False
			cantMove = [False, False, False, False]
			
			canAppend = True
			for oldPosition in oldPositions:
				if position == oldPosition:
					canAppend = False
					break
			if canAppend == True:
				oldPositions.insert(insertPosition, position.copy())
				insertPosition += 1
			while canMove == False:
				movement = random.randint(1, 4)
				
				if movement == 1:
					cantMove[0] = self.check_position([position[0], position[1] + 1], oldPositions)
					if cantMove[0] == False:
						self.maze[position[1]][position[0]][0] = 0
						position[1] += 1
						self.maze[position[1]][position[0]][1] = 0
						canMove = True
				
				if movement == 2:
					cantMove[1] = self.check_position([position[0], position[1] - 1], oldPositions)
					if cantMove[1] == False:
						self.maze[position[1]][position[0]][1] = 0
						position[1] -= 1
						self.maze[position[1]][position[0]][0] = 0
						canMove = True
				
				if movement == 3:
					cantMove[2] = self.check_position([position[0] - 1, position[1]], oldPositions)
					if cantMove[2] == False:
						self.maze[position[1]][position[0]][2] = 0
						position[0] -= 1
						self.maze[position[1]][position[0]][3] = 0
						canMove = True
				
				if movement == 4:
					cantMove[3] = self.check_position([position[0] + 1, position[1]], oldPositions)
					if cantMove[3] == False:
						self.maze[position[1]][position[0]][3] = 0
						position[0] += 1
						self.maze[position[1]][position[0]][2] = 0
						canMove = True
				
				if cantMove[0] and cantMove[1] and cantMove[2] and cantMove[3]:
					position = oldPositions[insertPosition - 2].copy()
					insertPosition -= 1
					canMove = True
			
			closedBox = self.check_closedBox()

	def __init__(self, mazeSize):
		self.create_maze(mazeSize)