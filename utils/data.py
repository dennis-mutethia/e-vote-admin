import csv, os

class Unit():
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name
        
    def __hash__(self):
        return hash((self.id, self.code, self.name))

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented
        return (self.id, self.code, self.name) == (other.id, other.code, other.name)
    
#county_id,county_code,county_name,constituency_id,constituency_code,constituency_name,ward_id,ward_code,ward_name,polling_station_id,polling_station_code,polling_station_name
class Data:
    def __init__(self):
        self.dir = 'data'
        
    def get_counties(self): 
        try:       
            # List all files with the .csv extension
            counties = [os.path.splitext(f)[0] for f in os.listdir(self.dir) if f.endswith('.csv')]
            return counties
        except Exception as e:
            print(e)
            return []
        
    def get_constituencies(self, county):
        try:
            # Specify the path to your CSV file
            file_path = f'{self.dir}/{county}.csv'

            # Read the CSV file
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file) 
                constituencies = set()
                for row in csv_reader:
                    constituencies.add(Unit(row[3],row[4],row[5]))
                return constituencies
        except Exception as e:
            print(e)
            return []
    
    def get_wards(self, county, constituency_id):
        try:
            # Specify the path to your CSV file
            file_path = f'{self.dir}/{county}.csv'

            # Read the CSV file
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)             
                wards = set()
                for row in csv_reader:
                    if row[3] == constituency_id:
                        wards.add(Unit(row[6],row[7],row[8]))
                return wards
        except Exception as e:
            print(e)
            return set()
    
    def get_polling_stations(self, county, ward_id):
        try:
            # Specify the path to your CSV file
            file_path = f'{self.dir}/{county}.csv'

            # Read the CSV file
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)            
                polling_stations = set()
                for row in csv_reader:
                    if row[6] == ward_id:
                        polling_stations.add(Unit(row[9],row[10],row[11]))
                return polling_stations
        except Exception as e:
            print(e)
            return set()