import pygame
from User.define_user import User
from User.define_character import Character

class define_Controls:
	def __init__(self):
		self.quitGame = pygame.K_ESCAPE
		
		self.moveDown = [pygame.K_s, pygame.K_DOWN]
		self.moveUp = [pygame.K_w, pygame.K_UP]
		self.moveLeft = [pygame.K_a, pygame.K_LEFT]
		self.moveRight = [pygame.K_d, pygame.K_RIGHT]
		
		self.changedisplayStats = [pygame.K_f, pygame.K_F3]
		self.changeTime = pygame.K_c
		self.fullscreen = pygame.K_F11

Controls = define_Controls()
