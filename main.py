# the main Pygame file used to code the core mechanics of the game

import pygame as pg # imports the pygame library and allows for the library to be referred to as pg throughout the code
import sys # imports the system-specific parameters and functions
import os # imports the operating system which allows to define the path to access the necessary resources (e.g. images, audio)
from sprites import * # imports all data defined in the sprites file
from settings import * # imports all data defined in the settings file
from database import * # imports all data defined in the database file
import math # imports the math library which allows for the use of key mathematical constants and operations
import random # imports the random library to provide elements of luck to the game (e.g. power ups, maze generation)
pg.font.init() # initialises the font module which allows for using text fonts
pg.mixer.init() # initialises the mixer module which allow for audio to be played

username = "" # defines the empty variable which stores the player's inputted username
password = "" # defines the empty variable which stores the player's inputted password
total_points = 0 # defines the empty variable which stores the player's points received in the game
level = 1 # defines the empty variable which stores the player's points received in the game
logged_in = False # defines the boolean variable which indicates whether the player is logged into the game with their account
player_username = "" # defines the empty variable which store the username of the current player that is logged in
WINDOW = pg.display.set_mode((WIDTH, HEIGHT)) # displays a window with the width and height defined in the settings file
pg.display.set_caption("MAZE HUNTER") # sets the name of the Pygame window to the name of the game

# defines the font type (freesansbold) and the varying font sizes used throughout the game
LARGE_FONT = pg.font.Font(None, 96)
MEDIUM_FONT = pg.font.Font(None, 64)
SMALL_FONT = pg.font.Font(None, 32)

# defines and renders all standard sections of text to be displayed in the game, along with their colour
username_label = SMALL_FONT.render("USERNAME:", True, LIGHT_GREY)
password_label = SMALL_FONT.render("PASSWORD:", True, LIGHT_GREY)
login_text = LARGE_FONT.render("LOGIN", True, WHITE)
sign_up_text = LARGE_FONT.render("SIGN UP", True, WHITE)
login_success = SMALL_FONT.render("YOU HAVE SUCCESSFULLY LOGGED IN", True, GREEN)
login_fail = SMALL_FONT.render("YOUR USERNAME OR PASSWORD IS INCORRECT", True, RED)
sign_up_success = SMALL_FONT.render("YOU HAVE SUCCESSFULLY SIGNED UP", True, GREEN)
sign_up_fail = SMALL_FONT.render("YOUR USERNAME HAS ALREADY BEEN TAKEN", True, RED)
leaderboard_text = LARGE_FONT.render("LEADERBOARD", True, WHITE)
leaderboard_rank = MEDIUM_FONT.render("RANK", True, DARK_BLUE)
leaderboard_player = MEDIUM_FONT.render("PLAYER", True, DARK_BLUE)
leaderboard_points = MEDIUM_FONT.render("POINTS", True, DARK_BLUE)
leaderboard_level = MEDIUM_FONT.render("LEVEL", True, DARK_BLUE)
game_start = MEDIUM_FONT.render("PRESS ANY KEY TO START", True, LIGHT_BLUE)
game_points_label = SMALL_FONT.render("POINTS:", True, WHITE)
game_level_label = SMALL_FONT.render("LEVEL:", True, WHITE)
game_hearts_label = SMALL_FONT.render("HEARTS:", True, WHITE)
game_stunned = SMALL_FONT.render("STUNNED!", True, RED)
game_coin = SMALL_FONT.render("COIN!", True, GREEN)
game_dizzy = SMALL_FONT.render("DIZZY!", True, RED)
game_freeze = SMALL_FONT.render("FREEZE!", True, GREEN)
game_trapped = SMALL_FONT.render("TRAPPED!", True, RED)
game_heart = SMALL_FONT.render("HEART!", True, GREEN)
game_win = LARGE_FONT.render("YOU WIN!", True, GREEN)
game_next_level = MEDIUM_FONT.render("NEXT LEVEL...", True, LIGHT_BLUE)
game_over = LARGE_FONT.render("GAME OVER!", True, RED)
game_total = MEDIUM_FONT.render("YOU SCORED A TOTAL OF...", True, LIGHT_BLUE)

def main_menu(): # defined the procedure for the main menu events of the game
  clock = pg.time.Clock() # a clock variable which computes the time passing between events in the game
  run = True # a boolean variable which keeps the game running until it is set to False
  while run: # a condition-controlled iterative loop which constantly checks for the different events in the code
    clock.tick(FPS) # limits the number of 'game' loop updates to 60 per second
    mouse_pos = pg.mouse.get_pos() # defines the coordinates of the mouse position as a tuple
    for event in pg.event.get(): # a count-controlled iterative loop in which each event is monitored
      if event.type == pg.QUIT: # a selection statement which detects if the user has decided to quit the game
        run = False # exits the while loop
      if event.type == pg.MOUSEBUTTONDOWN: # checks if the mouse button has been pressed
        # checks if the mouse is hovering over any of the menu buttons and runs the corresponding infinite loop
        if START.circle_mouse_hover(mouse_pos):
          game(0, 1, 60)
        if EXIT.circle_mouse_hover(mouse_pos):
          run = False
        if LEADERBOARD.circle_mouse_hover(mouse_pos):
          leaderboard()
        if LOGIN.circle_mouse_hover(mouse_pos):
          login()
        if SIGN_UP.circle_mouse_hover(mouse_pos):
          sign_up()
    main_menu_drawing() # calls the main menu drawing function to draw all required graphics onto the window
  pg.quit() # quits the code
  sys.exit() # exits the system

def main_menu_drawing(): # defined the procedure for all main menu drawing to be done to the game window
  WINDOW.blit(MENU_BACKGROUND,(0, 0))# displays the menu background image starting at the top-left of the window
  # displays my main start menu title graphic and buttons, positioned according to the design
  WINDOW.blit(TITLE,(300, 10)) # displays the title graphic
  # draws each main menu button onto the screen
  START.draw()
  EXIT.draw()
  LEADERBOARD.draw()
  LOGIN.draw()
  SIGN_UP.draw()
  pg.display.update() # updates the game window to display all new drawings

def game(total_points, level, enemy_move_speed): # defined the procedure for the game events of the game
  clock = pg.time.Clock()
  run = True
  grid = create_maze()
  direction = -1 # a variable which stores the direction that the player is facing
  hunter_direction = -1 # a variable which stores the direction that the hunter is facing
  points = 0 # a variable which stores the points collected during the level
  hearts = 1 # a variable which stores the hearts remaining during the level
  enemy_move_counter = ENEMY_START_COUNTER # a variable which stores the progress of each hunter move, initially negative to give the player a head start
  player_is_stunned = False # a variable which indicates whether the player is stunned from walking into a wall
  player_is_trapped = False # a variable which indicates whether the player is in a trap
  player_is_dizzy = False # a variable which indicates whether the player is dizzy
  enemy_is_frozen = False # a variable which indicates whether the hunter is frozen
  game_has_started = False # a variable which indicates whether the level has started
  player_lost = False # a variable which indicates whether the player has lost
  player_won = False # a variable which indicates whether the player has won
  stun_start_time = 0 # a variable which stores the starting time of the stun
  trap_counter = 0 # a variable which stores the number of key presses registered while the player is in a trap
  dizzy_start_time = 0 # a variable which stores the starting time of the dizzy power up
  freeze_start_time = 0 # a variable which stores the start time of the freeze
  # creates instances of the player and enemy in the game, setting their starting cell in the top-left
  player = Player(0, 0, NINJA_IMAGE)
  hunter = Enemy(0, 0, HUNTER_IMAGE)
  # allocates a unique cell for each power up
  power_up_cells = [] # a list which stores the random cells to be used for each power up
  for x in range(16): # for each power up (5 lots of 3)
    power_up_column = 0
    power_up_row = 0
    power_up_cell = [0, 0]
    # checks that the selected cell is not a start cell, end cell, or an already selected cell
    while power_up_cell == [0, 0] or power_up_cell == [columns - 1, rows - 1] or power_up_cell in power_up_cells:
      # randomly generates a cell
      power_up_column = random.randint(0, columns - 1)
      power_up_row = random.randint(0, rows - 1)
      power_up_cell = [power_up_column, power_up_row]
    power_up_cells.append(power_up_cell) # appends the power up list with the random cell
  # globalises the power up variables which allows them to be accessed by the entire program
  global coin_1, coin_2, coin_3, trap_1, trap_2, trap_3, dizzy_1, dizzy_2, dizzy_3, freeze_1, freeze_2, freeze_3, heart_1, heart_2, heart_3
  # creates instances of each power up used for the game level
  coin_1 = Power_up(power_up_cells[0][0], power_up_cells[0][1], COIN_IMAGE)
  coin_2 = Power_up(power_up_cells[1][0], power_up_cells[1][1], COIN_IMAGE)
  coin_3 = Power_up(power_up_cells[2][0], power_up_cells[2][1], COIN_IMAGE)
  trap_1 = Power_up(power_up_cells[3][0], power_up_cells[3][1], TRAP_IMAGE)
  trap_2 = Power_up(power_up_cells[4][0], power_up_cells[4][1], TRAP_IMAGE)
  trap_3 = Power_up(power_up_cells[5][0], power_up_cells[5][1], TRAP_IMAGE)
  dizzy_1 = Power_up(power_up_cells[6][0], power_up_cells[6][1], DIZZY_IMAGE)
  dizzy_2 = Power_up(power_up_cells[7][0], power_up_cells[7][1], DIZZY_IMAGE)
  dizzy_3 = Power_up(power_up_cells[8][0], power_up_cells[8][1], DIZZY_IMAGE)
  freeze_1 = Power_up(power_up_cells[9][0], power_up_cells[9][1], FREEZE_IMAGE)
  freeze_2 = Power_up(power_up_cells[10][0], power_up_cells[10][1], FREEZE_IMAGE)
  freeze_3 = Power_up(power_up_cells[11][0], power_up_cells[11][1], FREEZE_IMAGE)
  heart_1 = Power_up(power_up_cells[12][0], power_up_cells[12][1], HEART_IMAGE)
  heart_2 = Power_up(power_up_cells[13][0], power_up_cells[13][1], HEART_IMAGE)
  heart_3 = Power_up(power_up_cells[14][0], power_up_cells[14][1], HEART_IMAGE)
  while run:
    clock.tick(FPS)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_DOWN or event.key == pg.K_UP or event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
          game_has_started = True # starts the game if the player has pressed an arrow key
        if not player_is_stunned and not player_is_trapped: # checks that the player is not stunned or trapped
          # takes the directional input and sets the variable with the corresponding direction
          if event.key == pg.K_DOWN:
            direction = 0
          elif event.key == pg.K_UP:
            direction = 1
          elif event.key == pg.K_LEFT:
            direction = 2
          elif event.key == pg.K_RIGHT:
            direction = 3
          else:
            direction = -1
          if player_is_dizzy: # checks if the player is dizzy
            direction = random.randint(0, 3) # randomises the player's direction, regardless of the initial input
            current_time = pg.time.get_ticks() # stores the current time in the game
            # checks if the elapsed time from the start of the power up to now is greater than or equal to the duration
            if current_time - dizzy_start_time >= DIZZY_DURATION: 
              player_is_dizzy = False  # player is no longer dizzy
          if not player.move(direction) and not game_has_started and not player_is_stunned: # checks if the player has ran into a wall, the game has not already started, and they are not already stunned
            player_is_stunned = True # player is stunned
            stun_start_time = pg.time.get_ticks()
    if player_is_stunned: # checks if player is stunned
      current_time = pg.time.get_ticks()
      if current_time - stun_start_time >= STUN_DURATION:
        player_is_stunned = False  # player is no longer stunned
    if game_has_started:
      enemy_move_counter += 1 # increments the progress of the hunter's next move by 1
    if enemy_is_frozen: # checks if the enemy is frozen
      enemy_move_counter -= 0.5 # decrements the progress of the hunter's next move by a half, essentially halving the hunter's speed
      current_time = pg.time.get_ticks()
      if current_time - freeze_start_time >= FREEZE_DURATION:
        enemy_is_frozen = False  # enemy is no longer frozen
    if enemy_move_counter >= enemy_move_speed: # checks if the progress of the hunter's next move is complete
      hunter_direction = hunter.chase_player(player) # hunter chases the player and the direction is stored
      enemy_move_counter = 0  # resets the move progress
      if coin_1.hit(grid[player.column][player.row]) and not coin_1.collected: # checks if the player has hit the power up, and it is not already collected
        coin_1.collected = True # power up has been collected
        points += 500 # increments the player's points by 500
        WINDOW.blit(game_coin, (740, 440)) # displays the power up message
        pg.display.update()
        pg.time.delay(POWER_UP_MESSAGE_TIME) # pauses the screen for a second
      if coin_2.hit(grid[player.column][player.row]) and not coin_2.collected:
        coin_2.collected = True
        points += 500
        WINDOW.blit(game_coin, (740, 440))
        pg.display.update()
        pg.time.delay(POWER_UP_MESSAGE_TIME)
      if coin_3.hit(grid[player.column][player.row]) and not coin_3.collected:
        coin_3.collected = True
        points += 500
        WINDOW.blit(game_coin, (740, 440))
        pg.display.update()
        pg.time.delay(POWER_UP_MESSAGE_TIME)
      if dizzy_1.hit(grid[player.column][player.row]) and not dizzy_1.collected:
        dizzy_1.collected = True
        player_is_dizzy = True # player is dizzy
        dizzy_start_time = pg.time.get_ticks() # sets the start time of the power up as the current time
      if dizzy_2.hit(grid[player.column][player.row]) and not dizzy_2.collected:
        dizzy_2.collected = True
        player_is_dizzy = True
        dizzy_start_time = pg.time.get_ticks()
      if dizzy_3.hit(grid[player.column][player.row]) and not dizzy_3.collected:
        dizzy_3.collected = True
        player_is_dizzy = True
        dizzy_start_time = pg.time.get_ticks()
      if freeze_1.hit(grid[player.column][player.row]) and not freeze_1.collected:
        freeze_1.collected = True
        enemy_is_frozen = True # enemy is frozen
        freeze_start_time = pg.time.get_ticks()
      if freeze_2.hit(grid[player.column][player.row]) and not freeze_2.collected:
        freeze_2.collected = True
        enemy_is_frozen = True
        freeze_start_time = pg.time.get_ticks()
      if freeze_3.hit(grid[player.column][player.row]) and not freeze_3.collected:
        freeze_3.collected = True
        enemy_is_frozen = True
        freeze_start_time = pg.time.get_ticks()
      if heart_1.hit(grid[player.column][player.row]) and not heart_1.collected:
        heart_1.collected = True
        hearts += 1 # increments the number of hearts by 1
        WINDOW.blit(game_heart, (740, 440))
        pg.display.update()
        pg.time.delay(POWER_UP_MESSAGE_TIME)
      if heart_2.hit(grid[player.column][player.row]) and not heart_2.collected:
        heart_2.collected = True
        hearts += 1
        WINDOW.blit(game_heart, (740, 440))
        pg.display.update()
        pg.time.delay(POWER_UP_MESSAGE_TIME)
      if heart_3.hit(grid[player.column][player.row]) and not heart_3.collected:
        heart_3.collected = True
        hearts += 1
        WINDOW.blit(game_heart, (740, 440))
        pg.display.update()
        pg.time.delay(POWER_UP_MESSAGE_TIME)
      if trap_1.hit(grid[player.column][player.row]) and not trap_1.collected:
        player_is_trapped = True # player is trapped
        if trap_counter < TRAP_DURATION: # checks if the player has not pressed a key enough times
          if event.type == pg.KEYDOWN:
            trap_counter += 1 # increments the progress of escaping the trap by 1
        else: 
          player_is_trapped = False # player is no longer trapped
          trap_1.collected = True
          trap_counter = 0 # resets the progress of escaping the trap
      if trap_2.hit(grid[player.column][player.row]) and not trap_2.collected:
        player_is_trapped = True
        if trap_counter < TRAP_DURATION:
          if event.type == pg.KEYDOWN:
            trap_counter += 1
        else:
          player_is_trapped = False
          trap_2.collected = True
          trap_counter = 0
      if trap_3.hit(grid[player.column][player.row]) and not trap_3.collected:
        player_is_trapped = True
        if trap_counter < TRAP_DURATION:
          if event.type == pg.KEYDOWN:
            trap_counter += 1
        else:
          player_is_trapped = False
          trap_3.collected = True
          trap_counter = 0
      if (player.column, player.row) == (columns - 1, rows - 1): # checks if the player is on the end cell
        player_won = True # player has won the level
        points += LEVEL_POINTS # increments the player's points by 2000
        total_points += points # increments the player's total points by the points for the level
      # checks if the hunter is on the player's cell, and that it is not the start cell
      elif grid[hunter.column][hunter.row] == grid[player.column][player.row] != grid[0][0]:
        hearts -= 1 # decrements the number of hearts by 1
      if hearts <= 0: # checks if the player has no hearts remaining
        player_lost = True # player has lost
        total_points += points
    game_drawing(grid, player_username, player, hunter, total_points, level, direction, hunter_direction, points, hearts, player_is_stunned, player_is_trapped, player_is_dizzy, enemy_move_speed, enemy_is_frozen, game_has_started, player_won, player_lost) # calls the drawing function to draw all required graphics onto the window
  pg.quit()
  sys.exit()
  
def game_drawing(grid, player_username, player, hunter, total_points, level, direction, hunter_direction, points, hearts, player_is_stunned, player_is_trapped,player_is_dizzy, enemy_move_speed, enemy_is_frozen, game_has_started, player_won, player_lost): # defines the procedure for all game drawing to be done to the game window
  WINDOW.fill(BLACK) # fills the window with black
  for y in range(rows):
    for x in range(columns):
      grid[x][y].draw() # draws the cell in the grid corresponding the the row and column number
  WINDOW.blit(game_points_label, (10, 10)) # displays the points label
  game_points = SMALL_FONT.render(str(points), True, WHITE) # renders the surface which stores the current points
  WINDOW.blit(game_points, (110, 10)) # displays the current points
  WINDOW.blit(game_level_label, (10, 210)) # displays the level label
  game_level = SMALL_FONT.render(str(level), True, WHITE) # renders the surface which stores the current level
  WINDOW.blit(game_level, (100, 210)) # displays the current level
  WINDOW.blit(game_hearts_label, (10, 410)) # displays the hearts label
  game_hearts = SMALL_FONT.render(str(hearts), True, WHITE) # renders the surface which stores the current hearts
  WINDOW.blit(game_hearts, (130, 410)) # displays the current hearts
  if player_is_trapped: # checks if the player is trapped
    WINDOW.blit(game_trapped, (740, 40)) # displays the trapped message
  elif player_is_stunned: # checks if the player is stunned
    WINDOW.blit(game_stunned, (740, 140)) # displays the stunned message
  if enemy_is_frozen: # checks if the enemy is frozen
    WINDOW.blit(game_freeze, (740, 240)) # displays the frozen message
  if player_is_dizzy: # checks if the player is dizzy
    WINDOW.blit(game_dizzy, (740, 340)) # displays the dizzy message
  # checks if the power up has not been collected, and if so draws it onto the maze
  if not coin_1.collected:
    coin_1.draw()
  if not coin_2.collected:
    coin_2.draw()
  if not coin_3.collected:
    coin_3.draw()
  if not trap_1.collected:
    trap_1.draw()
  if not trap_2.collected:
    trap_2.draw()
  if not trap_3.collected:
    trap_3.draw()
  if not dizzy_1.collected:
    dizzy_1.draw()
  if not dizzy_2.collected:
    dizzy_2.draw()
  if not dizzy_3.collected:
    dizzy_3.draw()
  if not freeze_1.collected:
    freeze_1.draw()
  if not freeze_2.collected:
    freeze_2.draw()
  if not freeze_3.collected:
    freeze_3.draw()
  if not heart_1.collected:
    heart_1.draw()
  if not heart_2.collected:
    heart_2.draw()
  if not heart_3.collected:
    heart_3.draw()
  player.draw(direction) # draws the player with their updated position
  hunter.draw(hunter_direction) # draws the hunter with their updated position
  if not game_has_started: # checks if the game has not started
    WINDOW.blit(game_start, (170, 200)) # displays the game start message
  pg.display.update()
  if player_won: # checks if the player has won
    WINDOW.blit(game_win, (290, 200)) # displays the game win message
    pg.display.update()
    pg.time.delay(3000) # pauses the screen for 3 seconds
    WINDOW.blit(game_next_level, (300, 300)) # displays the game next level message
    pg.display.update()
    pg.time.delay(3000)
    game(total_points, level + 1, enemy_move_speed - 2)
  elif player_lost: # checks if the player has lost
    WINDOW.blit(game_over, (230, 200)) # displays the game over message
    pg.display.update()
    pg.time.delay(3000)
    WINDOW.blit(game_total, (150, 300)) # displays the game total points message
    pg.display.update()
    pg.time.delay(3000)
    game_total_points = LARGE_FONT.render(str(total_points), True, LIGHT_BLUE)
    WINDOW.blit(game_total_points, (380, 400)) # displays the total points
    pg.display.update()
    pg.time.delay(3000)
    update_leaderboard(player_username, total_points, level) # updates the leaderboard with the logged in player's final points and level
    main_menu() # sends the player to the main menu

def leaderboard(): # defined the procedure for the leaderboard events of the game
  clock = pg.time.Clock()
  run = True
  table = leaderboard_info() # stores the contents of the leaderboard as a 2D array
  while run:
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False
      if event.type == pg.MOUSEBUTTONDOWN:
        # directs the player back to the main menu if the back button is pressed
        if BACK.circle_mouse_hover(mouse_pos):
          main_menu()
    leaderboard_drawing(table) # calls the leaderboard drawing function to draw all required graphics onto the window
  pg.quit()
  sys.exit()
  
def leaderboard_drawing(table): # defined the procedure for all leaderboard drawing to be done to the game window
  WINDOW.blit(MENU_BACKGROUND,(0, 0))
  BACK.draw() # draws the back button
  WINDOW.blit(LEADERBOARD_TABLE, (140, 100)) # draws the leaderboard table
  # draws each leaderboard label
  WINDOW.blit(leaderboard_text,(190, 25))
  WINDOW.blit(leaderboard_rank,(140, 100))
  WINDOW.blit(leaderboard_player,(315, 100))
  WINDOW.blit(leaderboard_points,(492, 100))
  WINDOW.blit(leaderboard_level,(670, 100))
  for rank in RANKS: # the count-controlled loop which iterates through each rank number
    rank_text = SMALL_FONT.render(str(rank), True, LIGHT_BLUE) # renders each rank number with the same font
    WINDOW.blit(rank_text, (220, 115 + (34 * rank))) # displays each rank number with an increasing y-coordinate for each box in the column
  for y in range(0, len(table)): # for the first three columns in the database (username, points and level)
    for x in range(0, 3): # for the first ten players in the database
      value = SMALL_FONT.render(str(table[y][x]), True, DARK_BLUE) # renders the individual data value from the array
      WINDOW.blit(value, (325 + (175 * x), 149 + (34 * y))) # displays the data value in the correct table box by moving it from the top left as required
  pg.display.update()

def login(): # defined the procedure for the login events of the game
  clock = pg.time.Clock()
  run = True
  entering_username = False # defines the variable which indicates whether the player is entering their username
  entering_password = False # defines the variable which indicates whether the player is entering their password
  username = ""
  password = ""
  login_result = None # defines the empty variable which stores the result of the login check
  while run:
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False        
      if event.type == pg.MOUSEBUTTONDOWN:
        # checks if the credential boxes contain anything and if the continue button has been clicked, meaning that the player has finished entering their credentials
        if CONTINUE.circle_mouse_hover(mouse_pos) and (username and password != ""): 
          login_result = login_check(username, password) # calls the login check using the inputted username and password as parameters
        if BACK.circle_mouse_hover(mouse_pos):
          main_menu()
        # checks if the username box has been clicked, meaning that the player is entering their username
        if USERNAME_BOX.rectangle_mouse_hover(mouse_pos):
          entering_username = True
          entering_password = False
        # checks if the password box has been clicked, meaning that the player is entering their password
        elif PASSWORD_BOX.rectangle_mouse_hover(mouse_pos):
          entering_username = False
          entering_password = True
        # if neither of the above cases are true, the player has clicked an empty space on the screen, meaning that they are not entering a detail
        else:
          entering_username = False
          entering_password = False
      if event.type == pg.KEYDOWN: # checks if a key has been pressed
        if event.key == pg.K_RETURN and (username and password != ""): # checks if the credential boxes contain anything and if the key being pressed is a return, meaning that the player has finished entering their credentials
          login_result = login_check(username, password)
        elif entering_username: # checks if the user is entering their username
          if event.key == pg.K_BACKSPACE: # checks if the key being pressed is a backspace
            username = username[:-1] # replaces the existing credential with the same text but without the last character
          # does not append anything to the username variable if it is already at its maximum length of 12
          elif len(username) == 12:
            pass
          else:
            username += event.unicode # coverts the key event type into a unicode character and adds it to the credential variable
        elif entering_password: # checks if the user is entering their password instead
          if event.key == pg.K_BACKSPACE: 
            password = password[:-1]
          # does not append anything to the password variable if it is already at its maximum length of 12
          elif len(password) == 12:
            pass
          else:
            password += event.unicode # appends the password with the inputted characters
    login_drawing(username, password, entering_username, entering_password, login_result) # calls the login drawing function to draw all required graphics onto the window
  pg.quit()
  sys.exit()
  
def login_drawing(username, password, entering_username, entering_password, login_result): # defined the procedure for all login drawing to be done to the game window
  WINDOW.blit(MENU_BACKGROUND,(0, 0))
  BACK.draw()
  CONTINUE.draw()
  USERNAME_BOX.draw()
  PASSWORD_BOX.draw()
  if not entering_username and username == "": # checks if the player is not entering their username and that nothing has been entered
    WINDOW.blit(username_label,(310, 190))
  if not entering_password and password == "": # checks if the player is not entering their password and that nothing has been entered
    WINDOW.blit(password_label,(310, 240))
  WINDOW.blit(login_text,(340, 50))
  username_input = SMALL_FONT.render(username, True, BLACK) # renders the username input surface with the current username text
  password_input = SMALL_FONT.render("*" * len(password), True, BLACK) # renders the password input surface with an asterisk for each password character
  WINDOW.blit(username_input, (310, 190))
  WINDOW.blit(password_input,(310, 240))
  if login_result == True: # checks if the user has successfully logged in
    WINDOW.blit(login_success, (250, 400))
    global player_username
    player_username = username # stores the inputted username as the logged in player
  elif login_result == False: # checks if the user has failed to log in
    WINDOW.blit(login_fail, (200, 400))
  pg.display.update()

def sign_up(): # defined the procedure for the sign up events of the game
  clock = pg.time.Clock()
  run = True
  entering_username = False
  entering_password = False
  username = ""
  password = ""
  sign_up_result = None
  while run:
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False
      if event.type == pg.MOUSEBUTTONDOWN:
        if CONTINUE.circle_mouse_hover(mouse_pos) and (username and password != ""):
          sign_up_result = sign_up_check(username, password) # calls the sign up check using the inputted username and password as parameters
        if BACK.circle_mouse_hover(mouse_pos):
          main_menu()
        if USERNAME_BOX.rectangle_mouse_hover(mouse_pos):
          entering_username = True
          entering_password = False
        elif PASSWORD_BOX.rectangle_mouse_hover(mouse_pos):
          entering_username = False
          entering_password = True
        else:
          entering_username = False
          entering_password = False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_RETURN and (username and password != ""):
          sign_up_result = sign_up_check(username, password)
        elif entering_username:
          if event.key == pg.K_BACKSPACE:
            username = username[:-1]
          elif len(username) == 12:
            pass
          else:
            username += event.unicode
        elif entering_password:
          if event.key == pg.K_BACKSPACE:
            password = password[:-1]
          elif len(password) == 12:
            pass
          else:
            password += event.unicode
    sign_up_drawing(username, password, entering_username, entering_password, sign_up_result) # calls the sign up drawing function to draw all required graphics onto the window
  pg.quit()
  sys.exit()
  
def sign_up_drawing(username, password, entering_username, entering_password, sign_up_result): # defined the procedure for all sign up drawing to be done to the game window
  WINDOW.blit(MENU_BACKGROUND,(0, 0))
  BACK.draw()
  CONTINUE.draw()
  USERNAME_BOX.draw()
  PASSWORD_BOX.draw()
  if not entering_username and username == "":
    WINDOW.blit(username_label,(310, 190))
  if not entering_password and password == "":
    WINDOW.blit(password_label,(310, 240))
  WINDOW.blit(sign_up_text,(310, 50))
  username_input = SMALL_FONT.render(username, True, BLACK) 
  password_input = SMALL_FONT.render("*" * len(password), True, BLACK)
  WINDOW.blit(username_input, (310, 190))
  WINDOW.blit(password_input,(310, 240))
  if sign_up_result == True:
    WINDOW.blit(sign_up_success, (250, 400))
    player_username = username
  elif sign_up_result == False:
    WINDOW.blit(sign_up_fail, (210, 400))
  pg.display.update()

# creates variables for loading all image files used within the game, importing them from the 'Resources' folder
# creates copies of the images with maintained transparency and converts their pixel formats to match the surface to improve performance 
START_IMAGE = pg.image.load(os.path.join("Resources", "start.png")).convert_alpha()
EXIT_IMAGE = pg.image.load(os.path.join("Resources", "exit.png")).convert_alpha()
LEADERBOARD_IMAGE = pg.image.load(os.path.join("Resources", "leaderboard.png")).convert_alpha()
LOGIN_IMAGE = pg.image.load(os.path.join("Resources", "login.png")).convert_alpha()
SIGN_UP_IMAGE = pg.image.load(os.path.join("Resources", "sign_up.png")).convert_alpha()
BACK_IMAGE = pg.image.load(os.path.join("Resources", "back.png")).convert_alpha()
CONTINUE_IMAGE = pg.image.load(os.path.join("Resources", "continue.png")).convert_alpha()
CREDENTIAL_BOX_IMAGE = pg.image.load(os.path.join("Resources", "credential_box.png")).convert_alpha()
MENU_BACKGROUND_IMAGE = pg.image.load(os.path.join("Resources", "menu_background.png")).convert_alpha()
TITLE_IMAGE = pg.image.load(os.path.join("Resources", "title.png")).convert_alpha()
LEADERBOARD_TABLE_IMAGE = pg.image.load(os.path.join("Resources", "leaderboard_table.png")).convert_alpha()
NINJA_IMAGE = pg.image.load(os.path.join("Resources", "ninja.png")).convert_alpha()
HUNTER_IMAGE = pg.image.load(os.path.join("Resources", "hunter.png")).convert_alpha()
COIN_IMAGE = pg.image.load(os.path.join("Resources", "coin.png")).convert_alpha()
TRAP_IMAGE = pg.image.load(os.path.join("Resources", "trap.png")).convert_alpha()
DIZZY_IMAGE = pg.image.load(os.path.join("Resources", "dizzy.png")).convert_alpha()
FREEZE_IMAGE = pg.image.load(os.path.join("Resources", "freeze.png")).convert_alpha()
HEART_IMAGE = pg.image.load(os.path.join("Resources", "heart.png")).convert_alpha()

#scales all non-button images used in game
MENU_BACKGROUND = pg.transform.scale(MENU_BACKGROUND_IMAGE, (WIDTH, HEIGHT))
TITLE = pg.transform.scale(TITLE_IMAGE, (300, 250))
LEADERBOARD_TABLE = pg.transform.scale(LEADERBOARD_TABLE_IMAGE, (700, 380))

pg.mixer.music.load(os.path.join("Resources", "music.mp3")) # loads the music audio file, importing it from the 'Resources' folder
pg.mixer.music.set_volume(0.7) # sets the volume of the music
pg.mixer.music.play(-1) # plays the music audio file (parameter of -1 causes the file to be infinitely looped)

if __name__ == "__main__": # a selection statement which confirms that the code only runs when the file is run directly
  create_leaderboard() # runs the leaderboard creation procedure
  main_menu() # runs the main event procedure
