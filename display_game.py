import pygame
from pygame.locals import *
from User.define_user import User
from User.define_character import Character
from Grid.define_grid import Grid

wallColor = (255, 255, 255)
memorywallColor = (195, 195, 195)
floorColor = (0, 0, 0)
defaultFont = pygame.font.Font(pygame.font.get_default_font(), round(User.DisplayWidth / 32))

def print_text(text, position, color = (255, 255, 255)):
	printed = defaultFont.render(text, True, color)
	printed_width, printed_height = printed.get_size()
	User.Display.blit(printed, (position[0] * printed_width, position[1] * printed_height))

def display_character():
		position = [Character.position[0] - Character.cameraPosition[0] + User.CenterDisplay[0], Character.position[1] - Character.cameraPosition[1] + User.CenterDisplay[1]]
		outlineRect = (round(position[0] - Character.width / 2), round(position[1] - Character.width / 2), Character.width, Character.width)
		pygame.draw.rect(User.Display,  wallColor, outlineRect)
		innerRect = (round(position[0] - Character.width / 2 * Character.outline), round(position[1] - Character.width / 2 * Character.outline), Character.width * Character.outline, Character.width * Character.outline)
		pygame.draw.rect(User.Display,  Character.color, innerRect)

def display_box(box, position, color):
	if box[0] == 1:
		pygame.draw.line(User.Display, color, (position[0], position[1] + Grid.boxSize), (position[0] + Grid.boxSize, position[1] + Grid.boxSize), Grid.wallWidth)
	if box[1] == 1:
		pygame.draw.line(User.Display, color, (position[0], position[1]), (position[0] + Grid.boxSize, position[1]), Grid.wallWidth)
	if box[2] == 1:
		pygame.draw.line(User.Display, color, (position[0], position[1]), (position[0], position[1] + Grid.boxSize), Grid.wallWidth)
	if box[3] == 1:
		pygame.draw.line(User.Display, color, (position[0] + Grid.boxSize, position[1]), (position[0] + Grid.boxSize, position[1] + Grid.boxSize), Grid.wallWidth)

def draw_maze(Maze, offset, color):
	for row in range(len(Maze.maze)):
		yPosition = row * Grid.boxSize - offset[1]
		if -Grid.boxSize > yPosition or User.DisplayHeight < yPosition:
			continue
		for column in range(len(Maze.maze)):
			xPosition = column * Grid.boxSize - offset[0]
			if -Grid.boxSize > xPosition or User.DisplayWidth < xPosition:
				continue
			display_box(Maze.maze[row][column], (xPosition, yPosition), color)

def display_grid():
	pygame.draw.rect(User.Display, floorColor, (0, 0, User.DisplayWidth, User.DisplayHeight))
	for x in range(-1, 2):
		for y in range(-1, 2):
			xOffset = Character.cameraPosition[0] + x * Grid.boxSize * Grid.mazeSize - (Character.gridPosition[0] - round(Grid.gridSize / 2)) * Grid.mazeSize * Grid.boxSize
			yOffset = Character.cameraPosition[1] + y * Grid.boxSize * Grid.mazeSize - (Character.gridPosition[1] - round(Grid.gridSize / 2)) * Grid.mazeSize * Grid.boxSize
			draw_maze(Grid.grid[Character.gridPosition[1] - y][Character.gridPosition[0] - x], [xOffset, yOffset], wallColor)

def display_memoryGrid():
	for oldPosition in Character.oldPositions:
		if isinstance(oldPosition[0], int):
			draw_maze(Grid.grid[oldPosition[0]][oldPosition[1]], [Character.cameraPosition[0], Character.cameraPosition[1]], memorywallColor)
			continue
		Maze = Grid.grid[oldPosition[0][1]][oldPosition[0][0]]
		xOffset = oldPosition[1][0] * Grid.boxSize - (Character.cameraPosition[0] - (oldPosition[0][0] - Character.startgridPosition[0]) * Grid.mazeSize * Grid.boxSize)
		if xOffset < -Grid.boxSize or xOffset > User.DisplayWidth + Grid.boxSize:
			continue
		yOffset = oldPosition[1][1] * Grid.boxSize - (Character.cameraPosition[1] - (oldPosition[0][1] - Character.startgridPosition[1]) * Grid.mazeSize * Grid.boxSize)
		if yOffset < -Grid.boxSize or yOffset > User.DisplayHeight + Grid.boxSize:
			continue
		display_box(Maze.maze[oldPosition[1][1]][oldPosition[1][0]], [xOffset, yOffset], memorywallColor)

	for curerentPosition in Character.currentPositions:
		Maze = Grid.grid[curerentPosition[0][1]][curerentPosition[0][0]]
		xOffset = curerentPosition[1][0] * Grid.boxSize - (Character.cameraPosition[0] - (curerentPosition[0][0] - Character.startgridPosition[0]) * Grid.mazeSize * Grid.boxSize)
		if xOffset < -Grid.boxSize or xOffset > User.DisplayWidth + Grid.boxSize:
			continue
		yOffset = curerentPosition[1][1] * Grid.boxSize - (Character.cameraPosition[1] - (curerentPosition[0][1] - Character.startgridPosition[1]) * Grid.mazeSize * Grid.boxSize)
		if yOffset < -Grid.boxSize or yOffset > User.DisplayHeight + Grid.boxSize:
			continue
		display_box(Maze.maze[curerentPosition[1][1]][curerentPosition[1][0]], [xOffset, yOffset], wallColor)

def display_game():
	User.Display.fill((0, 0, 0))
	display_memoryGrid()
	display_character()
	pygame.display.set_caption(f'{User.clock.get_fps() :.1f}')
	
