# a separate file to store the values of all constant values used throughout the code

WIDTH, HEIGHT = 900, 500 # defines the width and height of the game window

MAZE_SIZE = 500 # defines the size of the game's mazes
CELL_SIZE = 25 # defines the size of each cell in the game's mazes
CHARACTER_SIZE = 25 # defines the size of each character sprite

# defines the RGB values for every colour used in the game
BLACK = (15, 21, 26)
DARK_GREY = (57, 62, 64)
LIGHT_GREY = (79, 94, 99)
DARK_BLUE = (45, 74, 92)
LIGHT_BLUE = (121, 159, 178)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FPS = 60 # defines the number of frames per second the game will update at

RANKS = [1,2,3,4,5,6,7,8,9,10] # defines the array containing every rank presented in the leaderboard table

POWER_UP_MESSAGE_TIME = 1000 # stored the time the game freezes for when a coin or heart is collected in milliseconds 

HUNTER_STARTING_SPEED = 30 # stores the speed of the hunter's during the first level of a a game
ENEMY_START_COUNTER = -120 # stores the hunter's movement delay at the start of each level in frames (equivalent to two seconds)
STUN_DURATION = 2000 # stores the duration of a stun in millisecond
TRAP_DURATION = 2 # stores the number of key presses required to escape a trap
DIZZY_DURATION = 3000 # stores the duration of a dizzy power up in milliseconds
FREEZE_DURATION = 5000 # stores the duration of a freeze in milliseconds
LEVEL_POINTS = 2000 # stores the number of points scored for completing a level
