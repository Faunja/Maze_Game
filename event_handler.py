import pygame
from pygame.locals import *
from User.define_user import User
from User.define_controls import Controls
from User.define_character import Character
from Grid.define_map import Map
from Display.define_display import Display

def event_keydown(keypress):
	if keypress == Controls.quitGame:
		User.playing = False

	if keypress in Controls.moveDown:
		Character.movement[1] = 1
		Controls.keypressed.append(keypress)
	if keypress in Controls.moveUp:
		Character.movement[1] = -1
		Controls.keypressed.append(keypress)
	if keypress in Controls.moveLeft:
		Character.movement[0] = -1
		Controls.keypressed.append(keypress)
	if keypress in Controls.moveRight:
		Character.movement[0] = 1
		Controls.keypressed.append(keypress)
	if keypress in Controls.holdRun and Character.tired == False:
		Character.running = True

	if keypress in Controls.changeCamera:
		Map.centeredMap = not Map.centeredMap
	if keypress in Controls.changedisplayStats:
		Display.displayStats = 1 - Display.displayStats
	if keypress in Controls.changeTime:
		Display.change_time()
	if keypress in Controls.fullscreen:
		Display.toggle_fullscreen()

def event_keyup(keypress):
	if keypress in Controls.moveDown:
		if Character.movement[1] == 1:
			Character.movement[1] = 0
			for key in Controls.keypressed:
				if key in Controls.moveUp:
					Character.movement[1] = -1
		Controls.keypressed.remove(keypress)
	if keypress in Controls.moveUp:
		if Character.movement[1] == -1:
			Character.movement[1] = 0
			for key in Controls.keypressed:
				if key in Controls.moveDown:
					Character.movement[1] = 1
		Controls.keypressed.remove(keypress)
	if keypress in Controls.moveLeft :
		if Character.movement[0] == -1:
			Character.movement[0] = 0
			for key in Controls.keypressed:
				if key in Controls.moveRight:
					Character.movement[0] = 1
		Controls.keypressed.remove(keypress)
	if keypress in Controls.moveRight :
		if Character.movement[0] == 1:
			Character.movement[0] = 0
			for key in Controls.keypressed:
				if key in Controls.moveLeft:
					Character.movement[0] = -1
		Controls.keypressed.remove(keypress)
	if keypress in Controls.holdRun:
		Character.running = False

def event_handler():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			event_keydown(event.key)
		if event.type == pygame.KEYUP:
			event_keyup(event.key)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				Map.centeredMap = False
				Map.grabbedMap = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				Map.grabbedMap = False
		if event.type == pygame.MOUSEWHEEL:
			Map.update_mapSize(-event.y)

		if event.type == pygame.VIDEORESIZE:
			width, height = event.size
			Display.change_displaySize(width, height)
		if event.type == pygame.QUIT:
			User.playing = False
	
	if Character.completedMaze == False:
		Character.update_character()
		Map.update_map()

