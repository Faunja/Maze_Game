import pygame
from pygame.locals import *
from User.define_user import User
from Display.define_display import Display
from User.define_character import Character
from Grid.define_map import Map
from Grid.define_grid import Grid

def print_text(text, position, color = (255, 255, 255)):
	printed = User.font.render(text, True, color)
	printed_width, printed_height = printed.get_size()
	if not Character.completedMaze:
		User.Display.blit(printed, (position[0] * printed_width, position[1] * printed_height))
	else:
		User.Display.blit(printed, (position[0] - printed_width / 2, position[1]))

def display_stats():
	timePrint = ""
	if Character.timeSpent[2] >= 1:
		timePrint = timePrint+str(Character.timeSpent[2])+":"
	if Character.timeSpent[1] < 10 and Character.timeSpent[2] >= 1:
		timePrint = timePrint+"0"+str(Character.timeSpent[1])+":"
	elif Character.timeSpent[1] >= 1:
		timePrint = timePrint+str(Character.timeSpent[1])+":"
	if Character.timeSpent[0] < 10 and (Character.timeSpent[1] >= 1 or Character.timeSpent[2] >= 1):
		timePrint = timePrint+"0"+str(round(Character.timeSpent[0], 2))
	else:
		timePrint = timePrint+str(round(Character.timeSpent[0], 2))
	print_text("Time Spent: "+timePrint, [0, 1], (120, 120, 255))
	xPosition = Character.mazePosition[0] + Character.gridPosition[0] * Grid.mazeSize - int(Grid.mazeSize / 2) - Character.startgridPosition[0] * Grid.mazeSize
	yPosition = -(Character.mazePosition[1] + Character.gridPosition[1] * Grid.mazeSize - int(Grid.mazeSize / 2) - Character.startgridPosition[1] * Grid.mazeSize)
	print_text("Position: ("+str(xPosition)+", "+str(yPosition)+")", [0, 2], (120, 120, 255))
	print_text("Grid Position: ("+str(Character.gridPosition[0])+", "+str(Character.gridPosition[1])+")", [0, 3], (120, 120, 255))
	print_text("Maze Position: ("+str(Character.mazePosition[0])+", "+str(Character.mazePosition[1])+")", [0, 4], (120, 120, 255))
	print_text("Stamina: "+str(round(Character.stamina[1] / Character.stamina[0] * 100, 3)), [0, 5], (120, 120, 255))
	if User.clock.get_fps() < 40:
		print_text("FPS: "+f'{User.clock.get_fps() :.1f}', [0, 0], (255, 60, 60))
		return
	print_text("FPS: "f'{User.clock.get_fps() :.1f}', [0, 0], (60, 255, 60))

def display_character():
	displayWidth = Character.width * Display.tileSize
	position = [(Character.position[0] - Map.cameraPosition[0]) * Display.tileSize + Display.CenterDisplay[0], (Character.position[1] - Map.cameraPosition[1]) * Display.tileSize + Display.CenterDisplay[1]]

	displayOutlineWidth = displayWidth * Character.outline
	outlineRect = (round(position[0] - displayWidth / 2), round(position[1] - displayWidth / 2), displayWidth, displayWidth)
	pygame.draw.rect(User.Display,  Display.wallColor, outlineRect)
	innerRect = (round(position[0] - displayOutlineWidth / 2), round(position[1] - displayOutlineWidth / 2), displayOutlineWidth, displayOutlineWidth)
	pygame.draw.rect(User.Display,  Character.color, innerRect)

def display_box(box, position, tilesize, color):
	displayboxSize = Grid.boxSize * tilesize
	displaywallWidth = round(Grid.wallWidth * tilesize)
	if displaywallWidth < 1:
		displaywallWidth = 1
	if box[0] == 1:
		pygame.draw.line(User.Display, color, (position[0], position[1] + displayboxSize), (position[0] + displayboxSize, position[1] + displayboxSize), displaywallWidth)
	if box[1] == 1:
		pygame.draw.line(User.Display, color, (position[0], position[1]), (position[0] + displayboxSize, position[1]), displaywallWidth)
	if box[2] == 1:
		pygame.draw.line(User.Display, color, (position[0], position[1]), (position[0], position[1] + displayboxSize), displaywallWidth)
	if box[3] == 1:
		pygame.draw.line(User.Display, color, (position[0] + displayboxSize, position[1]), (position[0] + displayboxSize, position[1] + displayboxSize), displaywallWidth)

def draw_maze(Maze, xPosition, yPosition):
	if Maze == None:
		return
	displayPosition = [Map.cameraPosition[0] * Display.tileSize, Map.cameraPosition[1] * Display.tileSize]
	displayboxSize = Grid.boxSize * Display.tileSize
	tileOffset = int((Grid.displaymazeSize - Grid.mazeSize) * displayboxSize / 2)
	for col in range(Grid.mazeSize):
		yOffset = col * displayboxSize - (displayPosition[1] - (yPosition - Character.startgridPosition[1]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[1] + tileOffset
		if yOffset < -displayboxSize or yOffset > Display.DisplayHeight + displayboxSize:
			continue
		for row in range(Grid.mazeSize):
			xOffset = row * displayboxSize - (displayPosition[0] - (xPosition - Character.startgridPosition[0]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[0] + tileOffset
			if xOffset < -displayboxSize or xOffset > Display.DisplayWidth + displayboxSize:
				continue
			display_box(Maze.maze[col][row], [xOffset, yOffset], Display.tileSize, Display.wallColor)

def draw_grid():
	for y in range(-Grid.displayChunk, Grid.displayChunk + 1):
		yPosition = Map.displaygridPosition[1] + y
		if yPosition < 0 or yPosition > Grid.gridSize - 1:
			continue
		for x in range(-Grid.displayChunk, Grid.displayChunk + 1):
			xPosition = Map.displaygridPosition[0] + x
			if xPosition < 0 or xPosition > Grid.gridSize - 1:
				continue
			Maze = Grid.grid[Map.displaygridPosition[1] + y][Map.displaygridPosition[0] + x]
			draw_maze(Maze, xPosition, yPosition)

def display_grid():
	displayPosition = [Map.cameraPosition[0] * Display.tileSize, Map.cameraPosition[1] * Display.tileSize]
	displayboxSize = Grid.boxSize * Display.tileSize
	tileOffset = int((Grid.displaymazeSize - Grid.mazeSize) * displayboxSize / 2)
	for y in range(-Grid.displayChunk, Grid.displayChunk + 1):
		yPosition = Map.displaygridPosition[1] + y
		if yPosition < 0 or yPosition > Grid.gridSize - 1:
			continue
		for x in range(-Grid.displayChunk, Grid.displayChunk + 1):
			xPosition = Map.displaygridPosition[0] + x
			if xPosition < 0 or xPosition > Grid.gridSize - 1:
				continue
			for box in Map.storedPositions[yPosition][xPosition]:
				Maze = Grid.grid[Map.displaygridPosition[1] + y][Map.displaygridPosition[0] + x]
				xOffset = box[0] * displayboxSize - (displayPosition[0] - (xPosition - Character.startgridPosition[0]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[0] + tileOffset
				if xOffset < -displayboxSize or xOffset > Display.DisplayWidth + displayboxSize:
					continue
				yOffset = box[1] * displayboxSize - (displayPosition[1] - (yPosition - Character.startgridPosition[1]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[1] + tileOffset
				if yOffset < -displayboxSize or yOffset > Display.DisplayHeight + displayboxSize:
					continue
				display_box(Maze.maze[box[1]][box[0]], [xOffset, yOffset], Display.tileSize, Display.memorywallColor)

	for currentPosition in Map.currentPositions:
		Maze = Grid.grid[currentPosition[0][1]][currentPosition[0][0]]
		xOffset = currentPosition[1][0] * displayboxSize - (displayPosition[0] - (currentPosition[0][0] - Character.startgridPosition[0]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[0] + tileOffset
		if xOffset < -displayboxSize or xOffset > Display.DisplayWidth + displayboxSize:
			continue
		yOffset = currentPosition[1][1] * displayboxSize - (displayPosition[1] - (currentPosition[0][1] - Character.startgridPosition[1]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[1] + tileOffset
		if yOffset < -displayboxSize or yOffset > Display.DisplayHeight + displayboxSize:
			continue
		display_box(Maze.maze[currentPosition[1][1]][currentPosition[1][0]], [xOffset, yOffset], Display.tileSize, Display.wallColor)

def display_game():
	pygame.draw.rect(User.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
	if Character.completedMaze == False:
		display_grid()
		display_character()
		if Display.displayStats:
			display_stats()
	else:
		pygame.draw.rect(User.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
		print_text("Good Job.", [Display.DisplayWidth / 2, Display.DisplayHeight / 2], Display.wallColor)
		timePrint = ""
		if Character.timeSpent[2] >= 1:
			timePrint = timePrint+str(Character.timeSpent[2])+":"
		if Character.timeSpent[1] < 10:
			timePrint = timePrint+"0"+str(Character.timeSpent[1])+":"
		elif Character.timeSpent[1] >= 1:
			timePrint = timePrint+str(Character.timeSpent[1])+":"
		if Character.timeSpent[0] < 10:
			timePrint = timePrint+"0"+str(round(Character.timeSpent[0], 2))
		else:
			timePrint = timePrint+str(round(Character.timeSpent[0], 2))
		print_text("Time Spent: "+timePrint, [Display.DisplayWidth / 2, 0], Display.wallColor)
	
