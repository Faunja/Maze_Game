import pygame, time
from pygame.locals import *

class define_User:
	def __init__(self, displayDifference):
		pygame.init()
		try:
			Display = pygame.display.get_desktop_sizes()
			self.ScreenSize = Display[0]
		except:
			self.ScreenSize = [1920, 1080]
		self.DisplayWidth = round(self.ScreenSize[1] * displayDifference)
		self.DisplayHeight = round(self.ScreenSize[1] * displayDifference)
		self.CenterDisplay = [round(self.DisplayWidth / 2), round(self.DisplayHeight / 2)]
		self.Display = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight))

		self.FPS = 60
		self.clock = pygame.time.Clock()
		self.playing = True

User = define_User(9 / 10)