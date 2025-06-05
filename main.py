import pygame, os, pickle
from pygame.locals import *
from User.define_user import User
from define_pickler import Pickler
from Display.display_game import display_game
from event_handler import event_handler

def main():
	Pickler.unpickle_data()
	while User.playing:
		User.deltaTime = User.clock.tick(User.FPS)
		if User.deltaTime == 0:
			User.deltaTime = 1
		if User.clock.get_fps() == 0:
			User.actualFPS = 60
		else:
			User.actualFPS = User.clock.get_fps()
		Pickler.check_pickle()
		event_handler()
		display_game()
		pygame.display.update() 
	Pickler.pickle_data()
	pygame.quit()

main()
