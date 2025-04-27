import pygame
from pygame.locals import *
from User.define_user import User
from User.define_controls import Controls
from User.define_character import Character

def event_handler():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == Controls.quitGame:
				User.playing = False
			if event.key == Controls.moveDown[0] or event.key == Controls.moveDown[1]:
				Character.movement[1] = 1
			if event.key == Controls.moveUp[0] or event.key == Controls.moveUp[1]:
				Character.movement[1] = -1
			if event.key == Controls.moveLeft[0] or event.key == Controls.moveLeft[1]:
				Character.movement[0] = -1
			if event.key == Controls.moveRight[0] or event.key == Controls.moveRight[1]:
				Character.movement[0] = 1

		if event.type == pygame.KEYUP:
			if (event.key == Controls.moveDown[0] or event.key == Controls.moveDown[1]) and Character.movement[1] == 1:
				Character.movement[1] = 0
			if (event.key == Controls.moveUp[0] or event.key == Controls.moveUp[1]) and Character.movement[1] == -1:
				Character.movement[1] = 0
			if (event.key == Controls.moveLeft[0] or event.key == Controls.moveLeft[1]) and Character.movement[0] == -1:
				Character.movement[0] = 0
			if (event.key == Controls.moveRight[0] or event.key == Controls.moveRight[1]) and Character.movement[0] == 1:
				Character.movement[0] = 0

		if event.type == pygame.QUIT:
			User.playing = False
	
	Character.move_character()