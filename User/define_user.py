import pygame, time
from pygame.locals import *

class define_User:
	def __init__(self):
		pygame.init()
		try:
			Display = pygame.display.get_desktop_sizes()
			self.ScreenSize = Display[0]
		except:
			self.ScreenSize = [1920, 1080]
		self.aspectRatio = self.ScreenSize[0] / self.ScreenSize[1]

		self.FPS = 60
		self.clock = pygame.time.Clock()
		self.playing = True
	
	def update_display(self, DisplayWidth, DisplayHeight, fullscreen):
		if fullscreen == False:
			self.Display = pygame.display.set_mode((DisplayWidth, DisplayHeight), pygame.RESIZABLE)
		else:
			self.Display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		if DisplayHeight < DisplayWidth:
			self.font = pygame.font.Font('Display/Fonts/m6x11.ttf', round(DisplayHeight / 32))
		else:
			self.font = pygame.font.Font('Display/Fonts/m6x11.ttf', round(DisplayWidth / 32))

User = define_User()