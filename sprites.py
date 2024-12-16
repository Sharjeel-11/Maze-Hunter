# a separate file to code all characters and objects included in the game (e.g. player character, enemy mob, power ups)

import pygame as pg
import sys
import os
import random
from main import *
from settings import *
from collections import deque # imports the double-ended queue structure from the collections library

columns = rows = int(MAZE_SIZE/CELL_SIZE) # defines the number of columns and rows in the game's maze by dividing the maze size by the cell size
stack = [] # initialises the stack which will manage cell backtracking by storing previously processed cells

class Player: # defines the player class which will store all attributed and methods of the player in the game
  def __init__(self, column, row, sheet): # defines the constructor method
    self.column = column
    self.row = row
    # stores the x and y coordinates of the player by multiplying the row and column number by the cell size
    self.x = column * CHARACTER_SIZE
    self.y = row * CHARACTER_SIZE
    self.frame_no = 0 # initialises the variable which stores the frame number of the sprite
    self.frames = [] # initialises the list which stores each frame in the sprite sheet
    for x in range(4):
      self.frames.append([]) # appends the list with an empty list for each direction
      for y in range(4):
        frame = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE)).convert_alpha() # creates a black surface with the same dimensions as the sprite
        frame.set_colorkey((0, 0, 0)) # makes the surface transparent by removing the black colour
        # blits the section of the sprite sheet with the corresponding frame onto the surface
        frame.blit(sheet, (0, 0), ((x * CHARACTER_SIZE), (y * CHARACTER_SIZE), CHARACTER_SIZE, CHARACTER_SIZE))
        self.frames[x].append(frame) # appends the direction-specific list with the frame
  
  def move(self, direction): # defines the function which confirms if the player can move and updates their coordinates if they can
    # stores the player's current position to be updated depending on the directional input
    new_column = self.column
    new_row = self.row
    self.cell = grid[new_column][new_row]
    wall = -1 # initialises the variable which stores the wall to be checked

    # updates the player's column and row number based on the direction, and updates the wall to be checked
    if direction == 0:
      new_row += 1
      wall = 0
    elif direction == 1:
      new_row -= 1
      wall = 2
    elif direction == 2:
      new_column -= 1
      wall = 1
    elif direction == 3:
      new_column += 1
      wall = 3
      
    if 0 <= new_column < columns and 0 <= new_row < rows: # checks if the new cell is not out of the maze
      if not grid[new_column][new_row].walls[wall]: # checks if the new cell is not blocked by a wall
        # updates the player's coordinates with their new position
        self.column = new_column
        self.row = new_row
        self.x = self.column * CHARACTER_SIZE
        self.y = self.row * CHARACTER_SIZE
        self.cell = grid[self.column][self.row]
        return True # move was successful
    else:
      return False # move was unsuccessful

  def draw(self, direction): # defines the function which draws the player sprite frame onto the screen
    self.frame_no = (self.frame_no + 0.15) % 4 # updates the progress of the next frame 
    self.frame = self.frames[direction][int(self.frame_no)] # stores the current frame from the 2D array
    self.rect = (self.x + 200, self.y)
    WINDOW.blit(self.frame, self.rect) # displays the frame

class Enemy: # defines the enemy class which will store all attributes and methods of the hunter in the game
  def __init__(self, column, row, sheet):
    self.column = column
    self.row = row
    self.x = column * CELL_SIZE
    self.y = row * CELL_SIZE
    self.frame_no = 0
    self.frames = []
    for x in range(4):
      self.frames.append([])
      for y in range(4):
        frame = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE)).convert_alpha()
        frame.set_colorkey((0, 0, 0))
        frame.blit(sheet, (0, 0), ((x * CHARACTER_SIZE), (y * CHARACTER_SIZE), CHARACTER_SIZE, CHARACTER_SIZE))
        self.frames[x].append(frame)

  def find_shortest_path(self, player): # defines the method which calculates the shortest path to the player using a BFS
    start_cell = grid[self.column][self.row] # stores the hunter's current cell as the start cell
    player_cell = grid[player.column][player.row] # stores the player's current cell as the end cell
    visited = set() # stores all visited cells in a set
    queue = deque([(start_cell, [])])  # uses a double-ended queue to store each cell processed, along with the shortest path to that cell

    while queue: # while the queue contains any cells
      current_cell, path = queue.popleft() # removes the left-most cell from the queue, and stores the cell and path
      visited.add(current_cell) # appends the visited set with the removed cell
      if current_cell == player_cell: # if the cell processed is the final cell
        return path # returns the path to the player's cell      
      neighbours = current_cell.find_neighbours(current_cell) # stores the neighbours of the current cell
      for neighbour in neighbours: # for each neighbour
        if neighbour not in visited: # checks if the neighbour has not been visited
          # appends the queue with the neighbour, calculating the new path by adding the cell to the current path
          queue.append((neighbour, path + [neighbour])) 
  
  def chase_player(self, player): # defines the methods which moves the hunter towards the player
    path = self.find_shortest_path(player) # stores the shortest path from the hunter to the player
    hunter_direction = -1

    if path: # checks if there is a path from the hunter to the player
      next_cell = path[0]  # stores the first cell in the path
      dx = next_cell.column - self.column # calculates and stores the change in column number between the next cell and the current cell
      dy = next_cell.row - self.row # calculates and stores the change in row number between the next cell and the current cell
      # checks the position of the next cell relative to the current cell and sets the corresponding hunter direction
      if dx > 0:
        hunter_direction = 3
      elif dx < 0:
        hunter_direction = 2
      elif dy > 0:
        hunter_direction = 0
      elif dy < 0:
        hunter_direction = 1
      self.move(hunter_direction) # moves the hunter using the hunter direction

    return hunter_direction # returns the hunter direction

  def move(self, hunter_direction): # defines the method which moves the hunter and updates its coordinates
    new_column = self.column
    new_row = self.row
    self.cell = grid[new_column][new_row]
    wall = -1

    if hunter_direction == 0:
      new_row += 1
      wall = 0
    elif hunter_direction == 1:
      new_row -= 1
      wall = 2
    elif hunter_direction == 2:
      new_column -= 1
      wall = 1
    elif hunter_direction == 3:
      new_column += 1
      wall = 3

    self.column = new_column
    self.row = new_row
    self.x = self.column * CHARACTER_SIZE
    self.y = self.row * CHARACTER_SIZE
    self.cell = grid[self.column][self.row]

  def draw(self, hunter_direction):  # defines the function which draws the hunter sprite frame onto the screen
    self.frame_no = (self.frame_no + 0.15) % 4
    self.frame = self.frames[hunter_direction][int(self.frame_no)]
    self.rect = (self.x + 200, self.y)
    WINDOW.blit(self.frame, self.rect)

class Power_up:  # defines the power up class which will store all attributes and methods of power ups in the game 
  def __init__(self, column, row, power_up):
    self.column = column
    self.row = row
    self.x = column * CELL_SIZE
    self.y = row * CELL_SIZE
    self.power_up = power_up
    self.collected = False # indicates whether the power up has been collected
  
  def hit(self, cell): # defines the method which checks if the player has hit a power up
      if grid[self.column][self.row] == cell: # checks if the player's current cell is the same as the power up cell
        return True # power up has been hit
      else:
        return False # power up has not been hit

  def draw(self): # defines the function which draws the power up sprite onto the screen
    self.rect = (self.x + 200, self.y)
    WINDOW.blit(self.power_up, self.rect)

class Cell(): # defines the cell class which will store all attributes and methods of cells in the game's maze
  def __init__(self, column, row):
    # stores the x and y coordinates of the cell by multiplying the row and column number by the cell size
    self.column = column
    self.row = row
    self.x = column * CELL_SIZE
    self.y = row * CELL_SIZE
    self.visited = False # tracks if the cell has been visited by the algorithm
    self.current = False # tracks if the cell is the current cell the algorithm is working on
    self.walls = [True, True, True, True] # an array which stores the condition of each wall around the cell [top, right, bottom, left]
    self.neighbours = [] # an array which stores unvisited neighbour cells
    # initialises variables which stores references to neighbour cells
    self.top = 0
    self.right = 0
    self.bottom = 0
    self.left = 0
    self.next_cell = 0 # initialises the variable that stores the next cell to visit
    self.is_start = False # indicates if the current cell is the start cell
    self.is_end = False # indicates if the current cell is the end cell

  def draw(self): # defines the procedure which draws the cell onto the maze window
    # draws each cell in the correct colour and at the right position
    # uses an offset of 200 pixels to position the maze in the centre of the window
    if self.is_start: # checks if the cell is the start cell
        pg.draw.rect(WINDOW, LIGHT_BLUE, (self.x + 200, self.y, CELL_SIZE, CELL_SIZE)) # draws the start cell in light blue
    elif self.is_end: # checks if the cell is the end cell
        pg.draw.rect(WINDOW, DARK_BLUE, (self.x + 200, self.y, CELL_SIZE, CELL_SIZE)) # draws the end cell in dark blue
    else:
        pg.draw.rect(WINDOW, LIGHT_GREY, (self.x + 200, self.y, CELL_SIZE, CELL_SIZE)) # draws the other cells in light grey
    
    # draws each wall as a line in the correct position and orientation according to the directional references
    if self.walls[0]: # checks if there is a wall above the cell
        pg.draw.line(WINDOW, DARK_GREY, (self.x + 200, self.y), ((self.x + CELL_SIZE + 200), self.y), 1) # draws the top wall
    if self.walls[1]: # checks if there is a wall to the right of the cell
        pg.draw.line(WINDOW, DARK_GREY, ((self.x + CELL_SIZE + 200), self.y),((self.x + CELL_SIZE + 200), (self.y + CELL_SIZE)), 1) # draws the right wall
    if self.walls[2]: # checks if there is a wall below the cell
        pg.draw.line(WINDOW, DARK_GREY, ((self.x + CELL_SIZE + 200), (self.y + CELL_SIZE)),(self.x + 200, (self.y + CELL_SIZE)), 1) # draws the bottom wall
    if self.walls[3]: # checks if there is a wall to the left of the cell
        pg.draw.line(WINDOW, DARK_GREY, (self.x + 200, (self.y + CELL_SIZE)), (self.x + 200, self.y), 1) # draws the left wall

  def check_neighbours(self): # defines the function which calculates the positions of the cell's neighbours and determines whether they have been visited
    if int(self.y/CELL_SIZE) - 1 >= 0: # checks if there is a row above the current one
      self.top = grid[int(self.x/CELL_SIZE)][int(self.y/CELL_SIZE) - 1] # stores the position of the top neighbour
      if self.top.visited == False: # checks if the top neighbour has been visited
        self.neighbours.append(self.top) # appends the unvisited neighbours list with the neighbour
    if int(self.x/CELL_SIZE) + 1 <= columns - 1: # checks if there is a column to the right of the current one
      self.right = grid[int(self.x/CELL_SIZE) + 1][int(self.y/CELL_SIZE)] # stores the position of the right neighbour
      if self.right.visited == False: # checks if the right neighbour has been visited
        self.neighbours.append(self.right)
    if int(self.y/CELL_SIZE) + 1 <= rows - 1: # checks if there is a row below the current one
      self.bottom = grid[int(self.x/CELL_SIZE)][int(self.y/CELL_SIZE) + 1] # stores the position of the bottom neighbour
      if self.bottom.visited == False: # checks if the bottom neighbour has been visited
        self.neighbours.append(self.bottom)
    if int(self.x/CELL_SIZE) - 1 >= 0: # checks if there is a column to the left of the current one
      self.left = grid[int(self.x/CELL_SIZE) - 1][int(self.y/CELL_SIZE)] # stores the position of the left neighbour
      if self.left.visited == False: # checks if the left neighbour has been visited
        self.neighbours.append(self.left)

    if len(self.neighbours) > 0: # checks if there are any unvisited neighbours
      # makes the next cell to be visited a random choice between all unvisited neighbours
      self.next_cell = self.neighbours[random.randrange(0, len(self.neighbours))]
      return self.next_cell # returns the next cell
    else:
      return False # there are no unvisited neighbours

  def find_neighbours(self, current_cell): # defines the function which finds neighbouring cells for the hunter to travel to
    x, y = current_cell.x // CELL_SIZE, current_cell.y // CELL_SIZE # calculates the column and row number of the hunter
    neighbours = [] # initialises the array which stores all traversable neighbouring cells
    
    if y > 0 and not current_cell.walls[0]: # checks if the hunter has a top neighbour and is not blocked by a wall
      neighbours.append(grid[x][y - 1]) # appends the neighbours array with the neighbouring cell
    if x < columns - 1 and not current_cell.walls[1]: # checks if the hunter has a right neighbour and is not blocked by a wall
      neighbours.append(grid[x + 1][y])
    if y < rows - 1 and not current_cell.walls[2]: # checks if the hunter has a bottom neighbour and is not blocked by a wall
      neighbours.append(grid[x][y + 1])
    if x > 0 and not current_cell.walls[3]: # checks if the hunter has a left neighbour and is not blocked by a wall
      neighbours.append(grid[x - 1][y])

    return neighbours # returns the array of neighbours

def remove_wall(current_cell, next_cell): # defines the function which removes a wall between two cells
  # calculates the relative difference in position of the two cells by finding the difference in row and column number
  x_dif = int(current_cell.x/CELL_SIZE) - int(next_cell.x/CELL_SIZE)
  y_dif = int(current_cell.y/CELL_SIZE) - int(next_cell.y/CELL_SIZE)
  if x_dif == -1: # checks if the next cell is to the right of the current cell
    current_cell.walls[1] = False # removes current cell's right wall
    next_cell.walls[3] = False # removes next cell's left wall
  elif x_dif == 1: # checks if the next cell is to the left of the current cell
    current_cell.walls[3] = False # removes current cell's left wall
    next_cell.walls[1] = False # removes next cell's right wall
  elif y_dif == -1: # checks if the next cell is below the current cell
    current_cell.walls[2] = False # removes current cell's bottom wall
    next_cell.walls[0] = False # removes next cell's top wall
  elif y_dif == 1: # checks if the next cell is above the current cell
    current_cell.walls[0] = False # removes current cell's top wall
    next_cell.walls[2] = False # removes next cell's bottom wall

def create_maze(): # defines the function which creates the level's maze
  maze_created = False # initialises the boolean variable which indicates whether the maze is complete
  global grid
  grid = [] # initialises the array which will store the entire maze in a 2D format
  # uses count_controlled iteration to loop through every row and column to fill the grid with cells
  for x in range(columns): # for every row in the maze
    grid.append([]) # appends the grid with an empty array to store each cell in that row
    for y in range(rows): # for every column in the maze
      grid[x].append(Cell(x, y)) # appends the row array with an instance of the cell class for each cell in the row
  current_cell = grid[0][0] # sets the initial current cell as the starting cell of the maze (top-left)
  next_cell = 0 # re-initialises the variable which stores the next cell to visit
  grid[0][0].is_start = True  # sets the top-left cell of the maze to be the start cell
  grid[columns - 1][rows - 1].is_end = True  # sets the bottom-right cell to be the end cell
  while not maze_created: # iterates through the maze generation algorithm while the maze is not complete
    current_cell.visited = True # indicates that the cell has been visited
    current_cell.current = True # indicates that the cell is the current cell being processed
    # uses count_controlled iteration to loop through every row and column to draw every grid cell onto the window
    next_cell = current_cell.check_neighbours() # retrieves all unvisited neighbour cells and then stores a random cell between them
    if next_cell: # checks if there are any unvisited neighbours
      stack.append(current_cell) # pushes the current cell onto the stack to be retrieved later
      remove_wall(current_cell, next_cell) # removes the wall between the current cell and the chosen neighbour
      current_cell.current = False # indicates that the current cell is no longer the processing cell
      current_cell.neighbours = [] # empties the neighbours array
      current_cell = next_cell # sets the current cell to the chosen neighbour
    elif len(stack) > 0: # checks if the stack still contains any cells
      current_cell.current = False
      current_cell = stack.pop() # retrieves the most recent cell by popping it from the stack and storing it at the current cell
    elif len(stack) == 0: # checks if the stack is empty (there are no more cells to be processed)
      maze_created = True # indicates that the maze is complete    
  return grid

class Button(): # defines the button class from which all button instances will be generated
  def __init__(self, image, x, y, scale):
    width = image.get_width() # defines the width of the button
    height = image.get_height() # defines the height of the button
    self.image = pg.transform.scale(image, (int(width * scale), int(height * scale))) # defines the updated button by scaling the image
    self.x = x # defines the x coordinate of the centre of the button
    self.y = y # defines the y coordinate of the centre of the button
    self.rect = self.image.get_rect(center=(self.x, self.y)) # defines the button collision box using the centre of the button

  def draw(self): # defines the function which draws the button to the screen
    WINDOW.blit(self.image, self.rect) # updates the screen with the button

  def circle_mouse_hover(self, position): # defines the function which checks if the mouse is hovering over a circular button
    if int(math.hypot(position[0]-self.x, position[1]-self.y)) <= (self.rect.right - self.rect.left)//2: # checks if the distance from the centre of the circle is less than the circle radius
      return True # mouse is hovering over button
    return False # mouse is not hovering over button

  def rectangle_mouse_hover(self, position): # defines the function which checks if the mouse is hovering over a rectangular button
    if self.rect.left <= position[0] <= self.rect.right and self.rect.top <= position[1] <= self.rect.bottom: # checks if the mouse is within the box 
      return True 
    return False

# creates instances of the button class for each button used in game
START = Button(START_IMAGE, 450, 400, 0.5)
EXIT = Button(EXIT_IMAGE, 275, 400, 0.5)
LEADERBOARD = Button(LEADERBOARD_IMAGE, 625, 400, 0.5)
LOGIN = Button(LOGIN_IMAGE, 100, 100, 0.5)
SIGN_UP = Button(SIGN_UP_IMAGE, 800, 100, 0.5)
BACK = Button(BACK_IMAGE, 75, 425, 0.5)
CONTINUE = Button(CONTINUE_IMAGE, 450, 325, 0.35)
USERNAME_BOX = Button(CREDENTIAL_BOX_IMAGE, 450, 200, 1)
PASSWORD_BOX = Button(CREDENTIAL_BOX_IMAGE, 450, 250, 1)
