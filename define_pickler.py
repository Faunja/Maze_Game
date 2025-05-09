import os, pickle, time
from Display.define_display import Display
from Grid.define_grid import Grid
from Grid.define_map import Map
from User.define_character import Character

class define_pickler:
	def __init__(self):
		self.time = time.time()
		self.timePassed = 0
		self.maxTime = 60

	def pickle_data(self):
		if Character.completedMaze == False:
			if os.path.exists('Save_data') == False:
				os.mkdir('Save_data')
			with open('Save_data/Display.pkl', 'wb') as file:
				pickle.dump(Display, file)
			with open('Save_data/Grid.pkl', 'wb') as file:
				pickle.dump(Grid, file)
			with open('Save_data/Map.pkl', 'wb') as file:
				pickle.dump(Map, file)
			with open('Save_data/Character.pkl', 'wb') as file:
				pickle.dump(Character, file)
	
	def check_pickle(self):
		currentTime = time.time()
		self.timePassed += currentTime - self.time
		self.time = currentTime
		if self.timePassed > self.maxTime:
			self.pickle_data()
			self.timePassed = 0

Pickler = define_pickler()
