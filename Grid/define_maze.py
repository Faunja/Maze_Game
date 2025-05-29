import pygame, random, copy
from pygame.locals import *
from User.define_user import User

class define_Maze:
	def check_maze(self):
		if self.position[0] != self.size - 1 or self.position[1] != self.size - 1:
			return True
		return False

	def replace_numbers(self, firstNumber, secondNumber):
		if firstNumber < secondNumber:
			replacement = firstNumber
			replace = secondNumber
		else:
			replacement = secondNumber
			replace = firstNumber
		for number in range(self.size):
			if self.numbers[self.position[1]][number] == replace:
				self.numbers[self.position[1]][number] = replacement
	
	def create_maze(self):
		while self.check_maze():
			if self.siding and self.position[1] != self.size - 1:
				if random.randint(0, 2) and self.numbers[self.position[1]][self.position[0]] != self.numbers[self.position[1]][self.position[0] + 1]:
					self.maze[self.position[1]][self.position[0]][3] = 0
					self.maze[self.position[1]][self.position[0] + 1][2] = 0
					self.replace_numbers(self.numbers[self.position[1]][self.position[0]], self.numbers[self.position[1]][self.position[0] + 1])
			elif self.siding:
				if self.numbers[self.position[1]][self.position[0]] != self.numbers[self.position[1]][self.position[0] + 1]:
					self.maze[self.position[1]][self.position[0]][3] = 0
					self.maze[self.position[1]][self.position[0] + 1][2] = 0
					self.replace_numbers(self.numbers[self.position[1]][self.position[0]], self.numbers[self.position[1]][self.position[0] + 1])

			if self.flooring:
				if random.randint(0, 1):
					self.maze[self.position[1]][self.position[0]][0] = 0
					self.maze[self.position[1] + 1][self.position[0]][1] = 0
					self.numbers[self.position[1] + 1][self.position[0]] = self.numbers[self.position[1]][self.position[0]]
					self.holes[self.floorNumbers.index(self.numbers[self.position[1]][self.position[0]])] = True
				else:
					self.floorPositions[self.floorNumbers.index(self.numbers[self.position[1]][self.position[0]])].append(self.position.copy())
				if self.position[0] == self.size - 1:
					self.checkfloor = True
				else:
					if self.numbers[self.position[1]][self.position[0]] != self.numbers[self.position[1]][self.position[0] + 1]:
						if self.numbers[self.position[1]][self.position[0] + 1] not in self.floorNumbers:
							self.floorNumbers.append(self.numbers[self.position[1]][self.position[0] + 1])
							self.floorPositions.append([])
							self.holes.append(False)

				if self.checkfloor:
					for number in range(len(self.floorPositions)):
						if self.holes[number]:
							continue
						hole = random.choice(self.floorPositions[number])
						self.maze[hole[1]][hole[0]][0] = 0
						self.maze[hole[1] + 1][hole[0]][1] = 0
						self.numbers[hole[1] + 1][hole[0]] = self.numbers[hole[1]][hole[0]]
						self.holes[number] = True

					self.holes = [False]
					self.floorPositions = [[]]
					self.checkfloor = False

			self.position[0] += 1
			if self.check_maze():
				if self.position[0] == self.size - 1 and self.siding:
					self.position[0] = 0
					self.floorNumbers = [self.numbers[self.position[1]][self.position[0]]]
					self.siding = False
					self.flooring = True
					self.number = self.numbers[self.position[1]][self.position[0]]
				elif self.position[0] == self.size:
					self.position = [0, self.position[1] + 1]
					self.siding = True
					self.flooring = False

	def __init__(self, size):
		self.size = size
		
		self.maze = []
		self.numbers = []
		for row in range(self.size):
			self.maze.append([])
			self.numbers.append([])
			for column in range(self.size):
				self.maze[row].append([1, 1, 1, 1])
				self.numbers[row].append(row * self.size + column)
		self.position = [0, 0]

		self.siding = True
		self.flooring = False
		self.floorNumbers = [self.numbers[self.position[1]][self.position[0]]]
		self.holes = [False]
		self.floorPositions = [[]]
		self.checkfloor = False

		self.create_maze()
