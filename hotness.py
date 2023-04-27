import requests as req
import xmltodict
import sqlite3
from sqlite3 import Error
from datetime import date 

def sql_connection():       # Connect to the local database
    try:
        con = sqlite3.connect('bgghotness.db')
        return con
    except Error:
        print(Error)

def create_todays_table(con, execute_string):   # Create the database table to store today's hotness rankings
    cursorObj = con.cursor()
    cursorObj.execute(execute_string)
    con.commit()

def add_todays_games(con, todays_table, today, games):  # Add today's hotness games to the new table with the date, name, rank, and BGG ID
    cursorObj = con.cursor()
    for game in games:
        insert_string = 'INSERT INTO {todaystable} (Date, Rank, Name, ID) VALUES ("{today}", {rank}, "{name}", {id})'.format(todaystable = todays_table, today = today, rank = int(game[2]), name = game[0], id = int(game[1]))
        print(insert_string)
        cursorObj.execute(insert_string)
        con.commit()
        

today = date.today().strftime('%d-%m-%Y')   # Grab today's date in a friendly dd-mm-yyyy format

response = req.get("https://boardgamegeek.com/xmlapi2/hot?type=boardgame")  # API call to BGG's hotness endpoint
data = xmltodict.parse(response.content)    # Parse the XML to a dictionary

games = []

for item in data["items"]["item"]:  # Step through the items in the dict and add them to a list
    name = item['name']['@value']
    game_id = item['@id']
    rank = item['@rank']
    this_game = [name, game_id, rank]
    games.append(this_game)

todays_table = "tbl" + date.today().strftime('%d%m%Y')  # Create a valid table name for today's table
execute_string = "CREATE TABLE {} (Date text, Rank integer, Name text, ID integer)".format(todays_table) 

con = sql_connection()  # Call to connect to database
create_todays_table(con, execute_string)    # Call to create the new table for today 
add_todays_games(con, todays_table, today, games)   # Call to add today's games to the new table