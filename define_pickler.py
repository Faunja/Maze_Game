import os, pickle, time
from User.define_user import User
from User.define_character import Character
from Grid.define_map import Map
from Grid.define_grid import Grid
from Display.define_display import Display

class define_pickler:
	def __init__(self):
		self.time = time.time()
		self.timePassed = 0
		self.maxTime = 60
	
	def check_data(self, newData, oldData):
		newVariables = vars(newData)
		oldVariables = vars(oldData)
		for variable in newVariables:
			if variable in oldVariables:
				newVariables[variable] = oldVariables[variable]
	
	def unpickle_data(self):
		if os.path.exists('Save_data/Character.pkl'):
			with open('Save_data/Character.pkl', 'rb') as file:
				referenceData = pickle.load(file)
				self.check_data(Character, referenceData)
		if os.path.exists('Save_data/Map.pkl'):
			with open('Save_data/Map.pkl', 'rb') as file:
				referenceData = pickle.load(file)
				self.check_data(Map, referenceData)
		if os.path.exists('Save_data/Grid.pkl'):
			with open('Save_data/Grid.pkl', 'rb') as file:
				referenceData = pickle.load(file)
				self.check_data(Grid, referenceData)
		if os.path.exists('Save_data/Character.pkl'):
			with open('Save_data/Display.pkl', 'rb') as file:
				referenceData = pickle.load(file)
				self.check_data(Display, referenceData)
				User.update_display(Display.DisplayWidth, Display.DisplayHeight, Display.fullscreen)

	def pickle_data(self):
		if Character.completedMaze == False:
			if os.path.exists('Save_data') == False:
				os.mkdir('Save_data')
			with open('Save_data/Character.pkl', 'wb') as file:
				pickle.dump(Character, file)
			with open('Save_data/Map.pkl', 'wb') as file:
				pickle.dump(Map, file)
			with open('Save_data/Grid.pkl', 'wb') as file:
				pickle.dump(Grid, file)
			with open('Save_data/Display.pkl', 'wb') as file:
				pickle.dump(Display, file)
	
	def check_pickle(self):
		currentTime = time.time()
		self.timePassed += currentTime - self.time
		self.time = currentTime
		if self.timePassed > self.maxTime:
			self.pickle_data()
			self.timePassed = 0

Pickler = define_pickler()
