from flask_login import current_user
import os, psycopg2
import uuid

from utils.entities import Candidate, Constituency, County, Election, MyVote, PollingStation, Voter, Ward

class Db():
    def __init__(self):
        # Access the environment variables
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self.schema = os.getenv('DB_SCHEMA')
        
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as e:
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(**self.conn_params)        
    
    def insert_county(self, code, name):
        id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{code}-{name}')))
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.counties (id, code, name) VALUES (%s, %s, %s)"
                cursor.execute(query, (id, code, name))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_county(self, id, code, name):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE {self.schema}.counties SET code = %s, name = %s WHERE id = %s"
                cursor.execute(query, (code, name, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_counties(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH constituencies AS(
                    SELECT county_id, COUNT(*) AS ttl_constituencies FROM {self.schema}.constituencies 
                    GROUP BY county_id
                )
                SELECT id, code, name, ttl_constituencies
                FROM {self.schema}.counties
                LEFT JOIN constituencies ON counties.id = constituencies.county_id
                ORDER BY code
                """
                cursor.execute(query)
                data = cursor.fetchall()
                counties = []
                for datum in data:
                    counties.append(County(datum[0], datum[1], datum[2], datum[3]))
                
                return counties
        except Exception as e:
            print(e)
            return []            
    
    def insert_constituency(self, code, county_id, name):
        id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{code}-{county_id}-{name}')))
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.constituencies (id, code, county_id, name) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, code, county_id, name))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_constituency(self, id, code, county_id, name):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE {self.schema}.constituencies SET code = %s, county_id=%s, name = %s WHERE id = %s"
                cursor.execute(query, (code, county_id, name, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
      
    def get_constituencies(self, county_id=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH wards AS(
                    SELECT constituency_id, COUNT(*) AS ttl_wards FROM {self.schema}.wards 
                    GROUP BY constituency_id
                )
                SELECT constituencies.id, constituencies.code, constituencies.name, county_id, counties.name, ttl_wards
                FROM {self.schema}.constituencies
                JOIN {self.schema}.counties ON county_id = counties.id
                LEFT JOIN wards ON constituencies.id = wards.constituency_id                
                """
                params = []
                if county_id is not None:
                    query = f"{query} WHERE county_id = %s"
                    params.append(county_id)
                query = f"{query} ORDER BY code"
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                constituencies = []
                for datum in data:
                    constituencies.append(Constituency(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5]))
                                    
                return constituencies
        except Exception as e:
            print(e)
            return []
       
    def insert_ward(self, code, constituency_id, name):
        id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{code}-{constituency_id}-{name}')))
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.wards (id, code, constituency_id, name) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, code, constituency_id, name))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_ward(self, id, code, constituency_id, name):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE {self.schema}.wards SET code = %s, constituency_id=%s, name = %s WHERE id = %s"
                cursor.execute(query, (code, constituency_id, name, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
      
    def get_wards(self, constituency_id=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH stations AS(
                    SELECT ward_id, COUNT(*) AS ttl_stations FROM {self.schema}.polling_stations 
                    GROUP BY ward_id
                )
                SELECT wards.id, wards.code, wards.name, constituency_id, constituencies.name, ttl_stations
                FROM {self.schema}.wards
                JOIN {self.schema}.constituencies ON constituency_id = constituencies.id
                LEFT JOIN stations ON wards.id = stations.ward_id                
                """
                params = []
                if constituency_id is not None:
                    query = f"{query} WHERE constituency_id = %s"
                    params.append(constituency_id)
                query = f"{query} ORDER BY code"
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                wards = []
                for datum in data:
                    wards.append(Ward(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5]))
                                    
                return wards
        except Exception as e:
            print(e)
            return []
     
    def insert_polling_station(self, code, ward_id, name):
        id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{code}-{ward_id}-{name}')))
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.polling_stations (id, code, ward_id, name) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, code, ward_id, name))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_polling_station(self, id, code, ward_id, name):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE {self.schema}.polling_stations SET code = %s, ward_id=%s, name = %s WHERE id = %s"
                cursor.execute(query, (code, ward_id, name, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
      
    def get_polling_stations(self, ward_id=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                SELECT polling_stations.id, polling_stations.code, polling_stations.name, ward_id, wards.name
                FROM {self.schema}.polling_stations
                JOIN {self.schema}.wards ON ward_id = wards.id        
                """
                params = []
                if ward_id is not None:
                    query = f"{query} WHERE ward_id = %s"
                    params.append(ward_id)
                query = f"{query} ORDER BY code"
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                polling_stations = []
                for datum in data:
                    polling_stations.append(PollingStation(datum[0], datum[1], datum[2], datum[3], datum[4]))
                                    
                return polling_stations
        except Exception as e:
            print(e)
            return []
    
    def get_voter(self, id=None, fingerprint_hash=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""SELECT voters.id, id_number, first_name, last_name, other_name, phone, polling_station_id, ward_id, constituency_id, county_id 
                FROM {self.schema}.voters
                JOIN {self.schema}.polling_stations ON polling_station_id = polling_stations.id
                JOIN {self.schema}.wards ON polling_stations.ward_id = wards.id
                JOIN {self.schema}.constituencies ON wards.constituency_id = constituencies.id
                """
                if id is not None:
                    query = f"{query} WHERE voters.id = %s"
                    cursor.execute(query, (id,))
                else:
                    query = f"{query} WHERE fingerprint_hash = %s"
                    cursor.execute(query, (fingerprint_hash,))
                data = cursor.fetchone()
                if data:
                    return Voter(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
                else:
                    return None
        except Exception as e:
            print(e)
            return None

    def insert_sms_code(self, voter, code):
        id = str(uuid.uuid4())
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.sms_codes (id, voter_id, polling_station_id, code) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, voter.id, voter.polling_station_id, code))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_sms_code(self, voter_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"SELECT code FROM {self.schema}.sms_codes WHERE voter_id = %s AND status = 0 ORDER BY created_at DESC LIMIT 1"
                cursor.execute(query, (voter_id,))
                data = cursor.fetchone()
                if data:
                    return data[0]
                else:
                    return None
        except Exception as e:
            print(e)
            return None
    
    def update_sms_code_status(self, voter_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE {self.schema}.sms_codes SET status = 1 WHERE voter_id = %s"
                cursor.execute(query, (voter_id,))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_active_election(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""SELECT id, name 
                    FROM {self.schema}.elections 
                    WHERE id NOT IN(
                        SELECT election_id FROM {self.schema}.votes WHERE voter_id = %s
                    )
                    ORDER BY code ASC LIMIT 1
                """
                cursor.execute(query, (current_user.id,))
                data = cursor.fetchone()
                if data:
                    return Election(data[0], data[1])
                else:
                    return None
        except Exception as e:
            print(e)
            return None   
      
    def get_candidates(self, election_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                SELECT c.id, c.icon, running_mate_icon, unit, unit_id,
                CONCAT(v.first_name, ' ', v.last_name, ' ', v.other_name) AS name, 
                CONCAT(v2.first_name, ' ', v2.last_name, ' ', v2.other_name) AS running_mate_name,
                p.name AS party_name, p.icon AS party_icon
                FROM {self.schema}.candidates c
                JOIN {self.schema}.voters v ON v.id = c.voter_id
                JOIN {self.schema}.voters v2 ON v2.id = c.running_mate_voter_id
                JOIN {self.schema}.parties p ON p.id = c.party_id
                WHERE c.election_id = %s
                """
                cursor.execute(query, (election_id,))
                data = cursor.fetchall()
                candidates = []
                for datum in data:
                    candidates.append(Candidate(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8]))
                
                return candidates
        except Exception as e:
            print(e)
            return None
    
    def cast_vote(self, election_id, candidate_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""INSERT INTO {self.schema}.votes 
                (election_id, candidate_id, voter_id, polling_station_id, ward_id, constituency_id, county_id, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                cursor.execute(query, (election_id, candidate_id, current_user.id, current_user.polling_station_id, current_user.ward_id, current_user.constituency_id, current_user.county_id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def create_sms_codes_partition(self, polling_station_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""CREATE TABLE IF NOT EXISTS {self.schema}.sms_codes_{polling_station_id.replace('-', '_')} 
                PARTITION OF {self.schema}.sms_codes FOR VALUES IN ('{polling_station_id}')
                """
                cursor.execute(query)
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False 
    
    def create_votes_partition(self, polling_station_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""CREATE TABLE IF NOT EXISTS {self.schema}.votes_{polling_station_id.replace('-', '_')} 
                PARTITION OF {self.schema}.votes FOR VALUES IN ('{polling_station_id}')"""
                cursor.execute(query)
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False 
      
    def get_my_votes(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH votes AS(
                    SELECT votes.election_id, CONCAT(first_name, ' ', last_name, ' ', other_name) AS candidate_name, icon
                    FROM {self.schema}.votes 
                    LEFT JOIN {self.schema}.candidates ON candidate_id = candidates.id
                    LEFT JOIN {self.schema}.voters ON candidates.voter_id = voters.id
                    WHERE votes.voter_id = %s
                )
                SELECT elections.code, elections.name, candidate_name, icon
                FROM e_vote.elections 
                LEFT JOIN votes ON election_id = elections.id
                ORDER BY elections.code
                """
                cursor.execute(query, (current_user.id,))
                data = cursor.fetchall()
                my_votes = []
                for datum in data:
                    my_votes.append(MyVote(datum[0], datum[1], datum[2], datum[3]))
                
                return my_votes
        except Exception as e:
            print(e)
            return None