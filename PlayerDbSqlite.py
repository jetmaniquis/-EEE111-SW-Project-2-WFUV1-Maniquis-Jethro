import sqlite3
import csv
from tkinter import filedialog

class PlayerDbSqlite:
    def __init__(self, dbName='BasketballTeam.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                height TEXT NOT NULL,
                jersey INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                height TEXT NOT NULL,
                jersey INTEGER NOT NULL
            )
        ''')
        self.commit_close()

    def fetch_players(self):
        try:
            self.connect_cursor()
            self.cursor.execute('SELECT * FROM players')
            players = self.cursor.fetchall()

        # Convert the height column to string format
            players_with_height_as_string = [
            (str(player[0]), player[1], player[2], str(player[3]) + ' cm', str(player[4])) for player in players
        ]

            self.conn.close()
            return players_with_height_as_string

        except sqlite3.Error as e:
            print("SQLite error:", e)


    def id_exists(self, player_id):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM players WHERE id = ?', (player_id,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def insert_player(self, id, name, position, height, jersey_number):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO players VALUES (?, ?, ?, ?, ?)', 
                       (id, name, position, height, jersey_number))
        self.conn.commit()

    def delete_player(self, player_id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM players WHERE id = ?', (player_id,))
        self.commit_close()

    def update_player(self, new_player_id, new_name, new_position, new_height, new_jersey):
        self.connect_cursor()
        self.cursor.execute('''
        UPDATE players
        SET name = ?, position = ?, height = ?, jersey = ?
        WHERE id = ?
    ''', (new_name, new_position, new_height, new_jersey, new_player_id))
        self.conn.commit()
        self.commit_close()




    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_players()
        for entry in dbEntries:
            print(entry)
            filehandle.write(f"{entry[0]},{entry[1]},{entry[3]},{entry[2]},{entry[4]}\n")


    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", ".csv")])

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    player_id, player_name, position, height, jersey_number = row
                    self.insert_player(player_id, player_name, position, height, jersey_number)
            return True
        
        except Exception as e:
            print(f"Error importing data from CSV: {e}")
            return False
