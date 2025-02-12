import csv, os

class Unit():
    def __init__(self, id, code, name, parent=None, grand_parent=None, great_grand_parent=None, ttl_constituencies=0, ttl_wards=0, ttl_polling_stations=0):
        self.id = id
        self.code = int(code)
        self.name = name
        self.parent = parent
        self.grand_parent = grand_parent
        self.great_grand_parent = great_grand_parent
        self.ttl_constituencies = ttl_constituencies
        
    def __hash__(self):
        return hash((self.id, self.code, self.name))

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented
        return (self.id, self.code, self.name) == (other.id, int(other.code), other.name)
    
#county_id,county_code,county_name,constituency_id,constituency_code,constituency_name,ward_id,ward_code,ward_name,polling_station_id,polling_station_code,polling_station_name
class Data:
    def __init__(self):
        self.dir = 'data'
        
    def get_county_names(self): 
        try:       
            # List all files with the .csv extension
            names = [os.path.splitext(f)[0] for f in os.listdir(self.dir) if f.endswith('.csv')]
            return names
        except Exception as e:
            print(e)
            return []
        
    def get_counties(self):
        try:
            counties = set()
            for county_name in self.get_county_names():
                file_path = f'{self.dir}/{county_name}.csv'
                
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    
                    # Collect data for one county
                    county_data = next(csv_reader)  # Assuming first row contains county data
                    constituencies, wards, polling_stations = set(), set(), set()
                    
                    for row in csv_reader:
                        constituencies.add(row[3])
                        wards.add(row[6])
                        polling_stations.add(row[9])
                    
                    # Create and populate the county object
                    county = Unit(county_data[0], county_data[1], county_data[2])
                    county.ttl_constituencies = len(constituencies)
                    county.ttl_wards = len(wards)
                    county.ttl_polling_stations = len(polling_stations)
                    counties.add(county)
            
            return counties
        except Exception as e:
            print(f"Error processing counties: {e}")
            return set()  # Return an empty set for consistency with return type
    
    def get_constituencies(self, county_name=None):
        try:
            constituencies = set()
            county_names = [county_name] if county_name else self.get_county_names()
            for county_name in county_names:
                file_path = f'{self.dir}/{county_name}.csv'
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    current_constituency = None
                    wards = set()
                    polling_stations = set()
                    
                    for row in csv_reader:
                        constituency_name = row[5]
                        if current_constituency is None or current_constituency.name != constituency_name:
                            if current_constituency:
                                # Finish processing the previous constituency
                                current_constituency.parent = county_name
                                current_constituency.ttl_wards = len(wards)
                                current_constituency.ttl_polling_stations = len(polling_stations)
                                constituencies.add(current_constituency)
                            
                            # Start a new or first constituency
                            current_constituency = Unit(row[3], row[4], constituency_name)
                            wards = set([row[6]])
                            polling_stations = set([row[9]])
                        else:
                            # Add to existing constituency
                            wards.add(row[6])
                            polling_stations.add(row[9])

                    # Handle the last constituency in the file
                    if current_constituency:
                        current_constituency.parent = county_name
                        current_constituency.ttl_wards = len(wards)
                        current_constituency.ttl_polling_stations = len(polling_stations)
                        constituencies.add(current_constituency)

            return constituencies
        except Exception as e:
            print(f"An error occurred: {e}")
            return set()  # Return an empty set for consistency

    def get_wards(self, county_name=None, constituency_name=None):
        try:
            wards = set()
            constituency_names = set()
            county_names = [county_name] if county_name else self.get_county_names()
            
            for county_name in county_names:
                file_path = f'{self.dir}/{county_name}.csv'
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    current_ward = None
                    polling_stations = set()
                    
                    for row in csv_reader:
                        ward_name = row[8]
                        constituency_names.add(row[5])
                        if current_ward is None or current_ward.name != ward_name:
                            if current_ward:
                                # Finish processing the previous ward
                                current_ward.parent = row[5]
                                current_ward.grand_parent = county_name
                                current_ward.ttl_polling_stations = len(polling_stations)
                                wards.add(current_ward)
                            
                            # Start a new or first ward
                            current_ward = Unit(row[6], row[7], ward_name)
                            polling_stations = set([row[9]])
                        else:
                            # Add to existing polling_station
                            polling_stations.add(row[9])

                    # Handle the last constituency in the file
                    if current_ward:
                        current_ward.parent = row[5]
                        current_ward.grand_parent = county_name
                        current_ward.ttl_polling_stations = len(polling_stations)
                        wards.add(current_ward)

            # Filter wards if only a specific constituency was requested
            if constituency_name:
                wards = {ward for ward in wards if ward.parent == constituency_name}
            
            return wards, constituency_names
        except Exception as e:
            print(f"An error occurred: {e}")
            return set(), []  # Return an empty set for wards
        
    def get_polling_stations(self, county_name=None, constituency_name=None, ward_name = None):
        try:
            polling_stations = set()
            wards = set()
            ward_names = set()
            constituency_names = set()
            county_names = [county_name] if county_name else self.get_county_names()
            
            for county_name in county_names:
                file_path = f'{self.dir}/{county_name}.csv'
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    current_polling_station = None
                    
                    for row in csv_reader:
                        polling_station_name = row[11]
                        wards.add(Unit(row[6], row[7], row[8], row[5]))
                        constituency_names.add(row[5])
                        if current_polling_station is None or current_polling_station.name != polling_station_name:
                            if current_polling_station:
                                # Finish processing the previous ward
                                current_polling_station.parent = row[8]
                                current_polling_station.grand_parent = row[5]
                                current_polling_station.great_grand_parent = county_name
                                polling_stations.add(current_polling_station)
                            
                            # Start a new or first ward
                            current_polling_station = Unit(row[9], row[10], polling_station_name)

                    # Handle the last constituency in the file
                    if current_polling_station:
                        current_polling_station.parent = row[8]
                        current_polling_station.grand_parent = row[5]
                        current_polling_station.great_grand_parent = county_name
                        polling_stations.add(current_polling_station)

            ward_names = {ward.name for ward in wards}
            
            # Filter wards if only a specific constituency was requested
            if constituency_name:
                polling_stations = {polling_station for polling_station in polling_stations if polling_station.grand_parent == constituency_name}
                ward_names = {ward.name for ward in wards if ward.parent == constituency_name }
            if ward_name:
                polling_stations = {polling_station for polling_station in polling_stations if polling_station.parent == ward_name}
                        
            return polling_stations, ward_names, constituency_names
        except Exception as e:
            print(f"An error occurred: {e}")
            return set(), []  # Return an empty set for polling_stations