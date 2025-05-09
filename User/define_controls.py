import pygame

class define_Controls:
	def __init__(self):
		self.quitGame = pygame.K_ESCAPE
		
		self.moveDown = [pygame.K_s, pygame.K_DOWN]
		self.moveUp = [pygame.K_w, pygame.K_UP]
		self.moveLeft = [pygame.K_a, pygame.K_LEFT]
		self.moveRight = [pygame.K_d, pygame.K_RIGHT]
		self.holdRun = [pygame.K_LSHIFT, pygame.K_LCTRL]
		self.changeCamera = [pygame.K_c]
		self.changeTime = [pygame.K_t]

		self.changedisplayStats = [pygame.K_F3]
		self.fullscreen = [pygame.K_F11]

Controls = define_Controls()
