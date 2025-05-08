import pygame, os, pickle
from pygame.locals import *
from User.define_user import User
from define_pickler import Pickler
from Display.display_game import display_game
from event_handler import event_handler

def main():
	while User.playing:
		User.clock.tick(User.FPS)
		Pickler.check_pickle()
		event_handler()
		display_game()
		pygame.display.update()
	Pickler.pickle_data()
	pygame.quit()

main()
