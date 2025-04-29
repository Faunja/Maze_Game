import pygame
from pygame.locals import *
from User.define_user import User
from Display.define_display import Display
from User.define_character import Character
from Grid.define_grid import Grid

def print_text(text, position, color = (255, 255, 255)):
	printed = Display.font.render(text, True, color)
	printed_width, printed_height = printed.get_size()
	Display.Display.blit(printed, (position[0] * printed_width, position[1] * printed_height))

def display_FPS():
	if User.clock.get_fps() < 40:
		print_text(f'{User.clock.get_fps() :.1f}', [0, 0], (255, 60, 60))
		return
	print_text(f'{User.clock.get_fps() :.1f}', [0, 0], (60, 255, 60))

def display_character():
		position = [Character.position[0] - Character.cameraPosition[0] + Display.CenterDisplay[0], Character.position[1] - Character.cameraPosition[1] + Display.CenterDisplay[1]]
		outlineRect = (round(position[0] - Character.width / 2), round(position[1] - Character.width / 2), Character.width, Character.width)
		pygame.draw.rect(Display.Display,  Display.wallColor, outlineRect)
		innerRect = (round(position[0] - Character.width / 2 * Character.outline), round(position[1] - Character.width / 2 * Character.outline), Character.width * Character.outline, Character.width * Character.outline)
		pygame.draw.rect(Display.Display,  Character.color, innerRect)

def display_box(box, position, color):
	if box[0] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1] + Grid.boxSize), (position[0] + Grid.boxSize, position[1] + Grid.boxSize), Grid.wallWidth)
	if box[1] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1]), (position[0] + Grid.boxSize, position[1]), Grid.wallWidth)
	if box[2] == 1:
		pygame.draw.line(Display.Display, color, (position[0], position[1]), (position[0], position[1] + Grid.boxSize), Grid.wallWidth)
	if box[3] == 1:
		pygame.draw.line(Display.Display, color, (position[0] + Grid.boxSize, position[1]), (position[0] + Grid.boxSize, position[1] + Grid.boxSize), Grid.wallWidth)

def draw_maze(Maze, offset, color):
	for row in range(len(Maze.maze)):
		yPosition = row * Grid.boxSize - offset[1]
		if -Grid.boxSize > yPosition or Display.DisplayHeight < yPosition:
			continue
		for column in range(len(Maze.maze)):
			xPosition = column * Grid.boxSize - offset[0] + Display.ScreenOffset
			if -Grid.boxSize > xPosition or Display.DisplayWidth < xPosition:
				continue
			display_box(Maze.maze[row][column], (xPosition, yPosition), color)

def display_grid():
	for x in range(-1, 2):
		for y in range(-1, 2):
			xOffset = Character.cameraPosition[0] + x * Grid.boxSize * Grid.mazeSize - (Character.gridPosition[0] - round(Grid.gridSize / 2)) * Grid.mazeSize * Grid.boxSize
			yOffset = Character.cameraPosition[1] + y * Grid.boxSize * Grid.mazeSize - (Character.gridPosition[1] - round(Grid.gridSize / 2)) * Grid.mazeSize * Grid.boxSize
			draw_maze(Grid.grid[Character.gridPosition[1] - y][Character.gridPosition[0] - x], [xOffset, yOffset], Display.wallColor)

def display_memoryGrid():
	for x in range(-1, 2):
		xPosition = Character.gridPosition[0] + x
		for y in range(-1, 2):
			yPosition = Character.gridPosition[1] + y
			for box in Character.storedPositions[yPosition][xPosition]:
				Maze = Grid.grid[Character.gridPosition[1] + y][Character.gridPosition[0] + x]
				xOffset = box[0] * Grid.boxSize - (Character.cameraPosition[0] - (xPosition - Character.startgridPosition[0]) * Grid.mazeSize * Grid.boxSize) + Display.ScreenOffset
				if xOffset < -Grid.boxSize or xOffset > Display.DisplayWidth + Grid.boxSize:
					continue
				yOffset = box[1] * Grid.boxSize - (Character.cameraPosition[1] - (yPosition - Character.startgridPosition[1]) * Grid.mazeSize * Grid.boxSize)
				if yOffset < -Grid.boxSize or yOffset > Display.DisplayHeight + Grid.boxSize:
					continue
				display_box(Maze.maze[box[1]][box[0]], [xOffset, yOffset], Display.memorywallColor)

	for curerentPosition in Character.currentPositions:
		Maze = Grid.grid[curerentPosition[0][1]][curerentPosition[0][0]]
		xOffset = curerentPosition[1][0] * Grid.boxSize - (Character.cameraPosition[0] - (curerentPosition[0][0] - Character.startgridPosition[0]) * Grid.mazeSize * Grid.boxSize) + Display.ScreenOffset
		if xOffset < -Grid.boxSize or xOffset > Display.DisplayWidth + Grid.boxSize:
			continue
		yOffset = curerentPosition[1][1] * Grid.boxSize - (Character.cameraPosition[1] - (curerentPosition[0][1] - Character.startgridPosition[1]) * Grid.mazeSize * Grid.boxSize)
		if yOffset < -Grid.boxSize or yOffset > Display.DisplayHeight + Grid.boxSize:
			continue
		display_box(Maze.maze[curerentPosition[1][1]][curerentPosition[1][0]], [xOffset, yOffset], Display.wallColor)

def display_game():
	pygame.draw.rect(Display.Display, Display.floorColor, (0, 0, Display.DisplayWidth, Display.DisplayHeight))
	display_memoryGrid()
	display_character()
	if Display.displayFPS == 1:
		display_FPS()
	
