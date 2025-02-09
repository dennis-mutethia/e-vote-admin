
from flask_login import UserMixin

class UserLevel():
    ADMIN = 0
    COUNTRY = 1
    COUNTY = 2
    CONSTITUENCY = 3
    WARD = 4
    POLLING_STATION = 5

class User(UserMixin):
    def __init__(self, id, id_number, first_name, last_name, other_name, phone, password, polling_station_id, ward_id, constituency_id, county_id, level):
        self.id = id
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.phone = phone
        self.password = password
        self.polling_station_id = polling_station_id
        self.ward_id = ward_id
        self.constituency_id = constituency_id
        self.county_id = county_id
        self.level = level

class County():
    def __init__(self, id, code, name, ttl_constituencies):
        self.id = id
        self.code = int(code)
        self.name = name
        self.ttl_constituencies = ttl_constituencies

class Constituency():
    def __init__(self, id, county_id, name, ttl_wards):
        self.id = id
        self.county_id = county_id
        self.name = name

class Ward():
    def __init__(self, id, constituency_id, name, ttl_polling_stations):
        self.id = id
        self.constituency_id = constituency_id
        self.name = name
        self.ttl_polling_stations = ttl_polling_stations

class PollingStation():
    def __init__(self, id, ward_id, name):
        self.id = id
        self.ward_id = ward_id
        self.name = name
        
class Election():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Voter():
    def __init__(self, id, id_number, first_name, last_name, other_name, phone, polling_station_id, ward_id, constituency_id, county_id):
        self.id = id
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.phone = phone
        self.polling_station_id = polling_station_id
        self.ward_id = ward_id
        self.constituency_id = constituency_id
        self.county_id = county_id
        
class Candidate():
    def __init__(self, id, icon, running_mate_icon, unit, unit_id, name, running_mate_name, party_name, party_icon):
        self.id = id
        self.icon = icon
        self.running_mate_icon = running_mate_icon
        self.unit = unit
        self.unit_id = unit_id
        self.name = name
        self.running_mate_name = running_mate_name
        self.party_name = party_name
        self.party_icon = party_icon

class MyVote():
    def __init__(self, election_code, election_name, candidate_name, icon):
        self.election_code = election_code
        self.election_name = election_name
        self.candidate_name = candidate_name
        self.icon = icon