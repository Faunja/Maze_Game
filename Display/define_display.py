import pygame, os, pickle
from pygame.locals import *
from User.define_user import User
from Grid.define_grid import Grid

class define_Display:
	def __init__(self):
		self.fullscreen = False
		self.displayDifference = 4 / 5
		self.DisplayWidth = round(User.ScreenSize[0] * self.displayDifference)
		self.DisplayHeight = round(User.ScreenSize[1] * self.displayDifference)
		self.ScreenOffset = [0, 0]
		self.ScreenOffset[1] = 0
		self.ScreenOffset[0] = round((self.DisplayWidth - self.DisplayHeight) / 2)
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		
		self.displayStats = False
		self.nightTime = 1
		
		self.tileSize = self.DisplayHeight / Grid.displaymazeSize
		
		self.wallColors = [(0, 0, 0), (255, 255, 255)]
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColors = [(120, 120, 120), (135, 135, 135)]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColors = [(255, 255, 255), (0, 0, 0)]
		self.floorColor = self.floorColors[self.nightTime]

		User.update_display(self.DisplayWidth, self.DisplayHeight, self.fullscreen)
	
	def check_displaySize(self):
		if self.DisplayWidth < int(User.ScreenSize[0] / 4):
			self.DisplayWidth = int(User.ScreenSize[0] / 4)
		if self.DisplayHeight < int(User.ScreenSize[1] / 4):
			self.DisplayHeight = int(User.ScreenSize[1] / 4)
		if self.DisplayWidth > int(self.DisplayHeight * User.aspectRatio):
			self.DisplayWidth = int(self.DisplayHeight * User.aspectRatio)
		if self.DisplayHeight > int(self.DisplayWidth * User.aspectRatio):
			self.DisplayWidth = int(self.DisplayHeight / User.aspectRatio)

	def change_displaySize(self, newWidth, newHeight):
		self.DisplayWidth = newWidth
		self.DisplayHeight = newHeight
		self.check_displaySize()
		if self.DisplayHeight < self.DisplayWidth:
			self.ScreenOffset[1] = 0
			self.ScreenOffset[0] = round((self.DisplayWidth - self.DisplayHeight) / 2)
			self.tileSize = self.DisplayHeight / Grid.displaymazeSize
		else:
			self.ScreenOffset[1] = round((self.DisplayHeight - self.DisplayWidth) / 2)
			self.ScreenOffset[0] = 0
			self.tileSize = self.DisplayWidth / Grid.displaymazeSize
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		User.update_display(self.DisplayWidth, self.DisplayHeight, self.fullscreen)
	
	def toggle_fullscreen(self):
		self.fullscreen = not self.fullscreen
		if self.fullscreen:
			self.change_displaySize(User.ScreenSize[0], User.ScreenSize[1])
		else:
			self.change_displaySize(round(User.ScreenSize[0] * self.displayDifference), round(User.ScreenSize[1] * self.displayDifference))
		User.update_display(self.DisplayWidth, self.DisplayHeight, self.fullscreen)
	
	def change_time(self):
		self.nightTime = 1 - self.nightTime
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColor = self.floorColors[self.nightTime]

Display = define_Display()
