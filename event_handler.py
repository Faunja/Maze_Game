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
			if event.key in Controls.changedisplayMap:
				if Map.displayMap == False:
					Map.displayMap = True
					Character.movement = [0, 0]
				else:
					Map.displayMap = False
					Map.movement = [0, 0]
			if Map.displayMap == False:
				if event.key in Controls.moveDown:
					Character.movement[1] = 1
				if event.key in Controls.moveUp:
					Character.movement[1] = -1
				if event.key in Controls.moveLeft:
					Character.movement[0] = -1
				if event.key in Controls.moveRight:
					Character.movement[0] = 1
			else:
				if event.key in Controls.moveDown:
					Map.movement[1] = 1
				if event.key in Controls.moveUp:
					Map.movement[1] = -1
				if event.key in Controls.moveLeft:
					Map.movement[0] = -1
				if event.key in Controls.moveRight:
					Map.movement[0] = 1
			if event.key in Controls.changedisplayStats:
				Display.displayStats = 1 - Display.displayStats
			if event.key in Controls.changeTime:
				Display.change_time()
			if event.key in Controls.fullscreen:
				Display.toggle_fullscreen()

		if event.type == pygame.KEYUP:
			if Map.displayMap == False:
				if event.key in Controls.moveDown and Character.movement[1] == 1:
					Character.movement[1] = 0
				if event.key in Controls.moveUp and Character.movement[1] == -1:
					Character.movement[1] = 0
				if event.key in Controls.moveLeft and Character.movement[0] == -1:
					Character.movement[0] = 0
				if event.key in Controls.moveRight and Character.movement[0] == 1:
					Character.movement[0] = 0
			else:
				if event.key in Controls.moveDown and Map.movement[1] == 1:
					Map.movement[1] = 0
				if event.key in Controls.moveUp and Map.movement[1] == -1:
					Map.movement[1] = 0
				if event.key in Controls.moveLeft and Map.movement[0] == -1:
					Map.movement[0] = 0
				if event.key in Controls.moveRight and Map.movement[0] == 1:
					Map.movement[0] = 0

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				Map.grabbedMap = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				Map.grabbedMap = False

		if event.type == pygame.VIDEORESIZE:
			width, height = event.size
			Display.change_displaySize(width, height)
		if event.type == pygame.QUIT:
			User.playing = False
	
	if Character.completedMaze == False:
		if Map.displayMap == False:
			Character.move_character()
		Map.update_map()

