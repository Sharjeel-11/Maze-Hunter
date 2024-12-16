# a separate file to code all functions and procedures used to access and manipulate the game's SQL database

import sqlite3 # imports the SQL database library to allow for data inside the database to be accessed and manipulated as required
from main import * # imports all data defined in the main file

def create_leaderboard(): # defines the procedure which creates the leaderboard table the first time the game is run on a system
    with sqlite3.connect("Leaderboard.db") as db: # connects to the database using the SQL library
        cursor = db.cursor() # defines the cursor object which is used to access the database
        # creates the leaderboard table if it does not yet exist, with the four listed keys
        sql = "CREATE TABLE IF NOT EXISTS tblLeaderboard (Username text Primary Key, Password text, Points integer, Level integer)"  
        cursor.execute(sql) # executes the SQL statement using the cursor
        db.commit() # ensures that the changes made by the SQL statement to the database is permanent

def sign_up_check(username, password): # defines the function which checks if the player can sign up with their inputted credentials
  with sqlite3.connect("Leaderboard.db") as db:
        cursor = db.cursor()
        sql = "SELECT * FROM tblLeaderboard WHERE Username = ?" # selects all data from any row with the same username as the player's inputted username
        cursor.execute(sql, (username,)) # executes the SQL statement with the second parameter acting as the reference/s for the '?'/s in the statement
        existing_user = cursor.fetchall() # stores all results from the SQL statement in a new variable
        if existing_user: # checks if the new variable collected any data from the SQL statement (i.e. if there is already an existing user)
          return False # player cannot use their desired username
        else:
          new_credentials = (username, password) # stores the new inputted credentials as a single tuple
          # inserts a new row into the leaderboard with the player's inputted credentials
          sql = "INSERT INTO tblLeaderboard (Username, Password, Points, Level) VALUES (?, ?, 0, 1)" 
          cursor.execute(sql, new_credentials)
          db.commit()
          logged_in = True # indicates that the player has successfully logged into the game
          global player_username
          player_username = username # stores the username of the player that has currently logged in
          return True # player has successfully signed up

def login_check(username, password): # defines the function which checks if the player can log in with their inputted credentials
  with sqlite3.connect("Leaderboard.db") as db:
        cursor = db.cursor()
        # selects all data from any row with the same credentials as the player's inputted credentials
        sql = "SELECT * FROM tblLeaderboard WHERE Username = ? AND Password = ?"
        cursor.execute(sql, (username, password))
        existing_user = cursor.fetchall()
        if existing_user:
          logged_in = True
          global player_username
          player_username = username
          return True # player has successfully logged in
        else:
          return False # player has used incorrect credentials

def update_leaderboard(player, points, level): # defines the procedure which updates the leaderboard if the player has achieved a high score
  with sqlite3.connect("Leaderboard.db") as db:
        cursor = db.cursor()
        # updates the logged in player's most recent points value if it is greater than their current points
        sql = "UPDATE tblLeaderboard SET Points = ? WHERE Username = ? AND ? > Points"
        cursor.execute(sql, (points, player, points))
        # updates the logged in player's most recent level value if it is greater than their current level
        sql = "UPDATE tblLeaderboard SET Level = ? WHERE Username = ? AND ? > Level"
        cursor.execute(sql, (level, player, level))
        db.commit()

def leaderboard_info(): # defines the function which returns the most recent data from the game's leaderboard as a 2D array
  with sqlite3.connect("Leaderboard.db") as db:
        cursor = db.cursor()
        # selects all game-specific values for each player from the leaderboard in descending order of points; this is retrieved as a list containing tuples
        sql = "SELECT Username, Points, Level FROM tblLeaderboard ORDER BY Points DESC"  
        cursor.execute(sql)
        info = cursor.fetchall()
        return info # returns the information from the leaderboard
