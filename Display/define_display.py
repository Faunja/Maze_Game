import pygame, time
from pygame.locals import *
from User.define_user import User

class define_Display:
	def __init__(self):
		self.displayDifference = 9 / 10
		self.DisplayWidth = round(User.ScreenSize[0] * self.displayDifference)
		self.DisplayHeight = round(User.ScreenSize[1] * self.displayDifference)
		if self.DisplayWidth < self.DisplayHeight:
			self.DisplayWidth = self.DisplayHeight
		else:
			self.ScreenOffset = round((self.DisplayWidth - self.DisplayHeight) / 2)
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		self.Display = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight))
		self.font = pygame.font.Font('Display/Fonts/m6x11.ttf', round(self.DisplayHeight / 32))
		
		self.displayFPS = 0
		self.nightTime = 1
		
		self.wallColors = [(0, 0, 0), (255, 255, 255)]
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColors = [(120, 120, 120), (135, 135, 135)]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColors = [(255, 255, 255), (0, 0, 0)]
		self.floorColor = self.floorColors[self.nightTime]
	
	def change_time(self):
		self.nightTime = 1 - self.nightTime
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColor = self.floorColors[self.nightTime]

Display = define_Display()
