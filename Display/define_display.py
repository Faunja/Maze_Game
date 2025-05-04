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

		self.displayStats = 0
		self.nightTime = 1
		
		self.tileSize = self.DisplayHeight / Grid.displaymazeSize
		self.maptileSize = self.DisplayHeight / Grid.mapdisplaymazeSize
		self.wallColors = [(0, 0, 0), (255, 255, 255)]
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColors = [(120, 120, 120), (135, 135, 135)]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColors = [(255, 255, 255), (0, 0, 0)]
		self.floorColor = self.floorColors[self.nightTime]
		User.update_display(self.DisplayWidth, self.DisplayHeight, self.fullscreen)
	
	def change_displaySize(self, newWidth, newHeight):
		self.DisplayWidth = newWidth
		self.DisplayHeight = newHeight
		if self.DisplayHeight < self.DisplayWidth:
			self.ScreenOffset[1] = 0
			self.ScreenOffset[0] = round((self.DisplayWidth - self.DisplayHeight) / 2)
			self.tileSize = self.DisplayHeight / Grid.displaymazeSize
			self.maptileSize = self.DisplayHeight / Grid.mapdisplaymazeSize
		else:
			self.ScreenOffset[1] = round((self.DisplayHeight - self.DisplayWidth) / 2)
			self.ScreenOffset[0] = 0
			self.tileSize = self.DisplayWidth / Grid.displaymazeSize
			self.maptileSize = self.DisplayWidth / Grid.mapdisplaymazeSize
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
	
	def toggle_fullscreen(self):
		if self.fullscreen == False:
			self.fullscreen = True
		else:
			self.fullscreen = False
		User.update_display(self.DisplayWidth, self.DisplayHeight, self.fullscreen)
	
	def change_time(self):
		self.nightTime = 1 - self.nightTime
		self.wallColor = self.wallColors[self.nightTime]
		self.memorywallColor = self.memorywallColors[self.nightTime]
		self.floorColor = self.floorColors[self.nightTime]

if os.path.exists('Save_data/Display.pkl'):
	with open('Save_data/Display.pkl', 'rb') as file:
		Display = pickle.load(file)
		User.update_display(Display.DisplayWidth, Display.DisplayHeight, Display.fullscreen)
else:
	Display = define_Display()
