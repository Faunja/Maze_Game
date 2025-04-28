import pygame, time
from pygame.locals import *
from User.define_user import User

class define_Display:
	def __init__(self, displayDifference):
		self.DisplayWidth = round(User.ScreenSize[1] * displayDifference)
		self.DisplayHeight = round(User.ScreenSize[1] * displayDifference)
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		self.Display = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight))

Display = define_Display(9 / 10)