import pygame
from pygame.locals import *
from User.define_user import User
from Display.define_display import Display
from User.define_character import Character
from Grid.define_map import Map
from Grid.define_grid import Grid

def print_text(text, position, color = (255, 255, 255)):
	printed = Display.font.render(text, True, color)
	printed_width, printed_height = printed.get_size()
	if Character.completedMaze == False:
		Display.Display.blit(printed, (position[0] * printed_width, position[1] * printed_height))
	else:
		Display.Display.blit(printed, (position[0] - printed_width / 2, position[1]))

def display_stats():
	print_text("("+str(Character.gridPosition[0])+", "+str(Character.gridPosition[1])+")", [0, 1], (120, 120, 255))
	print_text("("+str(Character.mazePosition[0])+", "+str(Character.mazePosition[1])+")", [0, 2], (120, 120, 255))
	if User.clock.get_fps() < 40:
		print_text(f'{User.clock.get_fps() :.1f}', [0, 0], (255, 60, 60))
		return
	print_text(f'{User.clock.get_fps() :.1f}', [0, 0], (60, 255, 60))

def display_character():
	if Map.displayMap == False:
		displayWidth = Character.width * Display.tileSize
		position = [(Character.position[0] - Character.cameraPosition[0]) * Display.tileSize + Display.CenterDisplay[0], (Character.position[1] - Character.cameraPosition[1]) * Display.tileSize + Display.CenterDisplay[1]]
	else:
		displayWidth = Character.width * Display.maptileSize
		position = [(Character.position[0] - Map.mapPosition[0]) * Display.maptileSize + Display.CenterDisplay[0], (Character.position[1] - Map.mapPosition[1]) * Display.maptileSize + Display.CenterDisplay[1]]
	displayOutlineWidth = displayWidth * Character.outline
	outlineRect = (round(position[0] - displayWidth / 2), round(position[1] - displayWidth / 2), displayWidth, displayWidth)
	pygame.draw.rect(Display.Display,  Display.wallColor, outlineRect)
	innerRect = (round(position[0] - displayOutlineWidth / 2), round(position[1] - displayOutlineWidth / 2), displayOutlineWidth, displayOutlineWidth)
	pygame.draw.rect(Display.Display,  Character.color, innerRect)

def display_box(box, position, tilesize, color):
	displayboxSize = Grid.boxSize * tilesize
	displaywallWidth = round(Grid.wallWidth * tilesize)
	if box[0] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1] + displayboxSize), (position[0] + displayboxSize, position[1] + displayboxSize), displaywallWidth)
	if box[1] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1]), (position[0] + displayboxSize, position[1]), displaywallWidth)
	if box[2] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1]), (position[0], position[1] + displayboxSize), displaywallWidth)
	if box[3] == 1:
		pygame.draw.line(Display.Display, color, (position[0] + displayboxSize, position[1]), (position[0] + displayboxSize, position[1] + displayboxSize), displaywallWidth)

def display_grid():
	displayPosition = [Character.cameraPosition[0] * Display.tileSize, Character.cameraPosition[1] * Display.tileSize]
	displayboxSize = Grid.boxSize * Display.tileSize
	tileOffset = int((Grid.displaymazeSize - Grid.mazeSize) * displayboxSize / 2)
	for y in range(Grid.displayChunk - int(Grid.displayChunk / 2) - Grid.displayChunk, Grid.displayChunk - int(Grid.displayChunk / 2)):
		yPosition = Character.gridPosition[1] + y
		if yPosition < 0 or yPosition > Grid.gridSize - 1:
			continue
		for x in range(Grid.displayChunk - int(Grid.displayChunk / 2) - Grid.displayChunk, Grid.displayChunk - int(Grid.displayChunk / 2)):
			xPosition = Character.gridPosition[0] + x
			if xPosition < 0 or xPosition > Grid.gridSize - 1:
				continue
			for box in Map.storedPositions[yPosition][xPosition]:
				Maze = Grid.grid[Character.gridPosition[1] + y][Character.gridPosition[0] + x]
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

def display_map():
	displayPosition = [Map.mapPosition[0] * Display.maptileSize, Map.mapPosition[1] * Display.maptileSize]
	displayboxSize = Grid.boxSize * Display.maptileSize
	tileOffset = int((Grid.mapdisplaymazeSize - Grid.mazeSize) * displayboxSize / 2)
	for y in range(Grid.mapdisplayChunk - int(Grid.mapdisplayChunk / 2) - Grid.mapdisplayChunk, Grid.mapdisplayChunk - int(Grid.mapdisplayChunk / 2)):
		yPosition = Map.gridPosition[1] + y
		if yPosition < 0 or yPosition > Grid.gridSize - 1:
			continue
		for x in range(Grid.mapdisplayChunk - int(Grid.mapdisplayChunk / 2) - Grid.mapdisplayChunk, Grid.mapdisplayChunk - int(Grid.mapdisplayChunk / 2)):
			xPosition = Map.gridPosition[0] + x
			if xPosition < 0 or xPosition > Grid.gridSize - 1:
				continue
			for box in Map.storedPositions[yPosition][xPosition]:
				Maze = Grid.grid[Map.gridPosition[1] + y][Map.gridPosition[0] + x]
				xOffset = box[0] * displayboxSize - (displayPosition[0] - (xPosition - Character.startgridPosition[0]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[0] + tileOffset
				if xOffset < -displayboxSize or xOffset > Display.DisplayWidth + displayboxSize:
					continue
				yOffset = box[1] * displayboxSize - (displayPosition[1] - (yPosition - Character.startgridPosition[1]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[1] + tileOffset
				if yOffset < -displayboxSize or yOffset > Display.DisplayHeight + displayboxSize:
					continue
				display_box(Maze.maze[box[1]][box[0]], [xOffset, yOffset], Display.maptileSize, Display.wallColor)

def display_game():
	pygame.draw.rect(Display.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
	if Character.completedMaze == False:
		if Map.displayMap == False:
			display_grid()
		else:
			display_map()
		display_character()
		if Display.displayStats == 1:
			display_stats()
	else:
		pygame.draw.rect(Display.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
		print_text("Good Job.", [Display.DisplayWidth / 2, Display.DisplayHeight / 2], Display.wallColor)
	
