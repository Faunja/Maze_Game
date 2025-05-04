import pygame
from pygame.locals import *
from User.define_user import User
from User.define_controls import Controls
from User.define_character import Character
from Grid.define_map import Map
from Display.define_display import Display

def event_handler():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == Controls.quitGame:
				User.playing = False
			if event.key in Controls.moveDown:
				Character.movement[1] = 1
			if event.key in Controls.moveUp:
				Character.movement[1] = -1
			if event.key in Controls.moveLeft:
				Character.movement[0] = -1
			if event.key in Controls.moveRight:
				Character.movement[0] = 1
			if event.key in Controls.changedisplayStats:
				Display.displayStats = 1 - Display.displayStats
			if event.key == Controls.changeTime:
				Display.change_time()
			if event.key == Controls.fullscreen:
				Display.toggle_fullscreen()

		if event.type == pygame.KEYUP:
			if event.key in Controls.moveDown and Character.movement[1] == 1:
				Character.movement[1] = 0
			if event.key in Controls.moveUp and Character.movement[1] == -1:
				Character.movement[1] = 0
			if event.key in Controls.moveLeft and Character.movement[0] == -1:
				Character.movement[0] = 0
			if event.key in Controls.moveRight and Character.movement[0] == 1:
				Character.movement[0] = 0
		
		if event.type == pygame.VIDEORESIZE:
			width, height = event.size
			Display.change_displaySize(width, height)

		if event.type == pygame.QUIT:
			User.playing = False
	
	if Character.completedMaze == False:
		Character.move_character()
		Map.update_map()
