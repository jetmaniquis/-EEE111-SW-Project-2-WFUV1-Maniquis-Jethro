from PlayerDbEntry import PlayerDbEntry
import csv
import sqlite3
import json
class PlayerDb:
    def __init__(self, init=False, dbName='PlayerDb.csv'):
        self.dbName = dbName
        self.entries = []
        print('TODO: __init__')
        if init is False:
            # Adding initial entries if init is False
            self.entries = [
                PlayerDbEntry('1', 'Stephen Curry', 'Point Guard', '165 cm', '30'),
                PlayerDbEntry('2', 'Lebron James', 'Point Guard', '165 cm', '23'),
                PlayerDbEntry('3', 'Luka Doncic', 'Point Guard', '165 cm', '77')
            ]

    def fetch_players(self):  # Renamed from fetch_employees
        print('TODO: fetch_player')
        tupleList = [(entry.id, entry.name, entry.position, entry.height, entry.jersey) for entry in self.entries]
        return tupleList

    def insert_player(self, id, name, position, height, jersey):
        newEntry = PlayerDbEntry(id=id, name=name, position=position, height=height, jersey=jersey)
        self.entries.append(newEntry)
        print('TODO: insert_player')

    def delete_player(self, id):
        for entry in self.entries:
            if entry.id == id:
                self.entries.remove(entry)
        print('TODO: delete_player')

    def update_player(self, id, new_name, new_position, new_height, new_jersey):
        for entry in self.entries:
            if entry.id == id:
                entry.name = new_name
                entry.position = new_position
                entry.height = new_height
                entry.jersey = new_jersey
        print('TODO: update_employee')


    def id_exists(self, id):
        return any(entry.id == id for entry in self.entries)

    def export_csv(self):
        with open(self.dbName, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Name', 'Position', 'Height', 'Jersey']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.entries:
                writer.writerow({
                    'ID': entry.id,
                    'Name': entry.name,
                    'Position': entry.position,
                    'Height': entry.height,
                    'Jersey': entry.jersey
                })

    def import_csv(self, csv_filename):
        try:
            if not csv_filename.lower().endswith('.csv'):
                csv_filename += '.csv'

            with open(csv_filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    player_id, player_name, player_position, player_height, jersey_number = row
                    # Add logic to handle the data, e.g., insert into your database
                    self.insert_player(player_id, player_name, player_position, player_height, jersey_number)
            print('Data imported successfully')
            return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {csv_filename}')
            return False
        except Exception as e:
            print(f'Error importing data: {e}')
            return False
        
    def export_json(self, json_filename='PlayerDb.json'):
        data = [{'ID': entry.id,
                 'Name': entry.name,
                 'Position': entry.position,
                 'Height': entry.height,
                 'Jersey': entry.jersey} for entry in self.entries]

        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def import_json(self, json_filename):
        try:
            with open(json_filename, 'r') as json_file:
                data = json.load(json_file)

                for entry_data in data:
                    self.insert_player(entry_data['ID'], entry_data['Name'], entry_data['Position'],
                                       entry_data['Height'], entry_data['Jersey'])
                print('Data imported successfully from JSON file')
                return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {json_filename}')
            return False
        except Exception as e:
            print(f'Error importing data from JSON: {e}')
            return False
