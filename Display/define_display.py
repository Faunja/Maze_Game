import pygame, time
from pygame.locals import *
from User.define_user import User
from Grid.define_grid import Grid

class define_Display:
	def __init__(self):
		self.fullscreen = False
		self.displayDifference = 9 / 10
		self.DisplayWidth = round(User.ScreenSize[0] * self.displayDifference / Grid.mazeSize) * Grid.mazeSize
		self.DisplayHeight = round(User.ScreenSize[1] * self.displayDifference / Grid.mazeSize) * Grid.mazeSize
		self.ScreenOffset = [0, 0]
		self.ScreenOffset[1] = 0
		self.ScreenOffset[0] = round((self.DisplayWidth - self.DisplayHeight) / 2)
		self.tileSize = self.DisplayHeight / Grid.mazeSize
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		self.Display = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight), pygame.RESIZABLE)
		self.font = pygame.font.Font('Display/Fonts/m6x11.ttf', round(self.DisplayHeight / 32))
		
		self.displayStats = 0
		self.nightTime = 1
		
		self.wallColors = [(0, 0, 0), (255, 255, 255)]
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColors = [(120, 120, 120), (135, 135, 135)]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColors = [(255, 255, 255), (0, 0, 0)]
		self.floorColor = self.floorColors[self.nightTime]
	
	def change_displaySize(self, newWidth, newHeight):
		self.DisplayWidth = newWidth
		self.DisplayHeight = newHeight
		self.ScreenOffset[1] = 0
		self.ScreenOffset[0] = round((self.DisplayWidth - self.DisplayHeight) / 2)
		self.tileSize = self.DisplayHeight / Grid.mazeSize
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		self.font = pygame.font.Font('Display/Fonts/m6x11.ttf', round(self.DisplayHeight / 32))
	
	def toggle_fullscreen(self):
		if self.fullscreen == False:
			self.fullscreen = True
			self.Display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.change_displaySize(User.ScreenSize[0], User.ScreenSize[1])
		else:
			self.fullscreen = False
			self.Display = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight), pygame.RESIZABLE)
	
	def change_time(self):
		self.nightTime = 1 - self.nightTime
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColor = self.floorColors[self.nightTime]

Display = define_Display()
