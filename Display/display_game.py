import pygame
from pygame.locals import *
from User.define_user import User
from Display.define_display import Display
from User.define_character import Character
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
	displayWidth = Character.width * Display.tileSize
	displayOutlineWidth = displayWidth * Character.outline
	position = [(Character.position[0] - Character.cameraPosition[0]) * Display.tileSize + Display.CenterDisplay[0], (Character.position[1] - Character.cameraPosition[1]) * Display.tileSize + Display.CenterDisplay[1]]
	outlineRect = (round(position[0] - displayWidth / 2), round(position[1] - displayWidth / 2), displayWidth, displayWidth)
	pygame.draw.rect(Display.Display,  Display.wallColor, outlineRect)
	innerRect = (round(position[0] - displayOutlineWidth / 2), round(position[1] - displayOutlineWidth / 2), displayOutlineWidth, displayOutlineWidth)
	pygame.draw.rect(Display.Display,  Character.color, innerRect)

def display_box(box, position, color):
	displayboxSize = Grid.boxSize * Display.tileSize
	displaywallWidth = round(Grid.wallWidth * Display.tileSize)
	if box[0] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1] + displayboxSize), (position[0] + displayboxSize, position[1] + displayboxSize), displaywallWidth)
	if box[1] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1]), (position[0] + displayboxSize, position[1]), displaywallWidth)
	if box[2] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1]), (position[0], position[1] + displayboxSize), displaywallWidth)
	if box[3] == 1:
		pygame.draw.line(Display.Display, color, (position[0] + displayboxSize, position[1]), (position[0] + displayboxSize, position[1] + displayboxSize), displaywallWidth)

def draw_maze(Maze, offset, color):
	displayboxSize = Grid.boxSize * Display.tileSize
	tileOffset = int((Grid.displaymazeSize - Grid.mazeSize) * displayboxSize / 2)
	for row in range(len(Maze.maze)):
		yPosition = row * displayboxSize - offset[1] + Display.ScreenOffset[1] + tileOffset
		if -displayboxSize > yPosition or Display.DisplayHeight < yPosition:
			continue
		for column in range(len(Maze.maze)):
			xPosition = column * displayboxSize - offset[0] + Display.ScreenOffset[0] + tileOffset
			if -displayboxSize > xPosition or Display.DisplayWidth < xPosition:
				continue
			display_box(Maze.maze[row][column], (xPosition, yPosition), color)

def display_grid():
	displaycameraPosition = [Character.cameraPosition[0] * Display.tileSize, Character.cameraPosition[1] * Display.tileSize]
	displayboxSize = Grid.boxSize * Display.tileSize
	for x in range(-1, 2):
		if Character.gridPosition[1] + y < 0 or Character.gridPosition[1] + y > Grid.gridSize - 1:
			continue
		for y in range(-1, 2):
			if Character.gridPosition[0] + x < 0 or Character.gridPosition[0] + x > Grid.gridSize - 1:
				continue
			xOffset = displaycameraPosition[0] + x * displayboxSize * Grid.mazeSize - (Character.gridPosition[0] - round(Grid.gridSize / 2)) * Grid.mazeSize * displayboxSize + Display.ScreenOffset[0]
			yOffset = displaycameraPosition[1] + y * displayboxSize * Grid.mazeSize - (Character.gridPosition[1] - round(Grid.gridSize / 2)) * Grid.mazeSize * displayboxSize + Display.ScreenOffset[1]
			draw_maze(Grid.grid[Character.gridPosition[1] + y][Character.gridPosition[0] + x], [xOffset, yOffset], Display.wallColor)

def display_memoryGrid():
	displaycameraPosition = [Character.cameraPosition[0] * Display.tileSize, Character.cameraPosition[1] * Display.tileSize]
	displayboxSize = Grid.boxSize * Display.tileSize
	tileOffset = int((Grid.displaymazeSize - Grid.mazeSize) * displayboxSize / 2)
	for y in range(-1, 2):
		yPosition = Character.gridPosition[1] + y
		if yPosition < 0 or yPosition > Grid.gridSize - 1:
			continue
		for x in range(-1, 2):
			xPosition = Character.gridPosition[0] + x
			if xPosition < 0 or xPosition > Grid.gridSize - 1:
				continue
			for box in Character.storedPositions[yPosition][xPosition]:
				Maze = Grid.grid[Character.gridPosition[1] + y][Character.gridPosition[0] + x]
				xOffset = box[0] * displayboxSize - (displaycameraPosition[0] - (xPosition - Character.startgridPosition[0]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[0] + tileOffset
				if xOffset < -displayboxSize or xOffset > Display.DisplayWidth + displayboxSize:
					continue
				yOffset = box[1] * displayboxSize - (displaycameraPosition[1] - (yPosition - Character.startgridPosition[1]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[1] + tileOffset
				if yOffset < -displayboxSize or yOffset > Display.DisplayHeight + displayboxSize:
					continue
				display_box(Maze.maze[box[1]][box[0]], [xOffset, yOffset], Display.memorywallColor)

	for currentPosition in Character.currentPositions:
		Maze = Grid.grid[currentPosition[0][1]][currentPosition[0][0]]
		xOffset = currentPosition[1][0] * displayboxSize - (displaycameraPosition[0] - (currentPosition[0][0] - Character.startgridPosition[0]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[0] + tileOffset
		if xOffset < -displayboxSize or xOffset > Display.DisplayWidth + displayboxSize:
			continue
		yOffset = currentPosition[1][1] * displayboxSize - (displaycameraPosition[1] - (currentPosition[0][1] - Character.startgridPosition[1]) * Grid.mazeSize * displayboxSize) + Display.ScreenOffset[1] + tileOffset
		if yOffset < -displayboxSize or yOffset > Display.DisplayHeight + displayboxSize:
			continue
		display_box(Maze.maze[currentPosition[1][1]][currentPosition[1][0]], [xOffset, yOffset], Display.wallColor)

def display_game():
	pygame.draw.rect(Display.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
	if Character.completedMaze == False:
		display_memoryGrid()
		display_character()
		if Display.displayStats == 1:
			display_stats()
	else:
		pygame.draw.rect(Display.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
		print_text("Good Job.", [Display.DisplayWidth / 2, Display.DisplayHeight / 2], Display.wallColor)
	
