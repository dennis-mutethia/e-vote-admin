
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
    def __init__(self, id, code, name, county_id, county_name, ttl_wards):
        self.id = id
        self.code = int(code)
        self.name = name
        self.county_id = county_id
        self.county_name = county_name
        self.ttl_wards = ttl_wards

class Ward():
    def __init__(self, id, code, name, constituency_id, constituency_name, ttl_stations):
        self.id = id
        self.code = int(code)
        self.name = name
        self.constituency_id = constituency_id
        self.constituency_name = constituency_name
        self.ttl_stations = ttl_stations

class PollingStation():
    def __init__(self, id, code, name, ward_id, ward_name, ttl_voters):
        self.id = id
        self.code = int(code)
        self.name = name
        self.ward_id = ward_id
        self.ward_name = ward_name
        self.ttl_voters = ttl_voters
        
class Election():
    def __init__(self, id, code, name, ttl_candidates):
        self.id = id
        self.code = int(code)
        self.name = name
        self.ttl_candidates = ttl_candidates
        
class Party():
    def __init__(self, id, name, icon, ttl_candidates):
        self.id = id
        self.name = name
        self.icon = icon
        self.ttl_candidates = ttl_candidates

class Voter():
    def __init__(self, id, id_number, first_name, last_name, other_name, phone, polling_station_id, polling_station_name, ward, constituency, county):
        self.id = id
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.name = f'{first_name} {last_name} {other_name}'
        self.phone = phone
        self.polling_station_id = polling_station_id
        self.polling_station_name = polling_station_name
        self.ward = ward 
        self.constituency = constituency 
        self.county = county
 
class Candidate():
    def __init__(self, id, id_number, name, phone, icon, polling_station_name, ward_name, constituency_name, county_name, election_id, election_name, party_id, party_name, party_icon, running_mate_name, running_mate_icon):
        self.id = id
        self.id_number = id_number
        self.name = name
        self.phone = phone
        self.icon = icon
        self.polling_station_name = polling_station_name
        self.ward_name = ward_name
        self.constituency_name = constituency_name
        self.county_name = county_name
        self.election_id = election_id
        self.election_name = election_name
        self.party_id = party_id
        self.party_name = party_name
        self.party_icon = party_icon
        self.running_mate_name = running_mate_name
        self.running_mate_icon = running_mate_icon

class MyVote():
    def __init__(self, election_code, election_name, candidate_name, icon):
        self.election_code = election_code
        self.election_name = election_name
        self.candidate_name = candidate_name
        self.icon = icon