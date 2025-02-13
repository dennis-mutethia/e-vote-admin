
import os, psycopg2, uuid
from flask_login import current_user
from dotenv import load_dotenv

from utils.entities import Candidate, Constituency, County, Election, MyVote, Party, PollingStation, Voter, Ward

load_dotenv()

class Db():
    def __init__(self):
        # Access the environment variables
        # self.conn_params = {
        #     'host': os.getenv('DB_HOST'),
        #     'port': os.getenv('DB_PORT'),
        #     'database': os.getenv('DB_NAME'),
        #     'user': os.getenv('DB_USER'),
        #     'password': os.getenv('DB_PASSWORD')
        # }        
            
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                #self.conn = psycopg2.connect(**self.conn_params)
                self.conn = psycopg2.connect(f"postgres://{user}:{password}@{host}:{port}/{database}?sslmode=require")                
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as e:
            # Reconnect if the connection is invalid
            #self.conn = psycopg2.connect(**self.conn_params)  
            self.conn = psycopg2.connect(f"postgres://{user}:{password}@{host}:{port}/{database}?sslmode=require")      
    
    import os

    def create_tables(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                # Load SQL script
                script_path = 'db_schema.sql'
                with open(script_path, 'r') as sql_file:
                    sql_script = sql_file.read()
                
                # Execute script
                cursor.execute(sql_script)
                self.conn.commit()  # Don't forget to commit the transaction
                return True
        except Exception as e:
            print(f"An error occurred while creating tables: {e}")
            return False
    
    def insert_sms_code(self, voter, code):
        id = str(uuid.uuid4())
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO sms_codes (id, voter_id, polling_station_id, code) VALUES (%s, %s, %s, %s)"
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
                query = f"SELECT code FROM sms_codes WHERE voter_id = %s AND status = 0 ORDER BY created_at DESC LIMIT 1"
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
                query = f"UPDATE sms_codes SET status = 1 WHERE voter_id = %s"
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
                    FROM elections 
                    WHERE id NOT IN(
                        SELECT election_id FROM votes WHERE voter_id = %s
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
      
    def get_candidates(self, election_id, page=0):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                SELECT c.id, c.icon, running_mate_icon, unit, unit_id,
                CONCAT(v.first_name, ' ', v.last_name, ' ', v.other_name) AS name, 
                CONCAT(v2.first_name, ' ', v2.last_name, ' ', v2.other_name) AS running_mate_name,
                p.name AS party_name, p.icon AS party_icon
                FROM candidates c
                JOIN voters v ON v.id = c.voter_id
                JOIN voters v2 ON v2.id = c.running_mate_voter_id
                JOIN parties p ON p.id = c.party_id
                WHERE c.election_id = %s
                """
                params = [election_id]
                if page>0:
                    query = f"{query} LIMIT 50 OFFSET %s"
                    params.append((page - 1)*50)
                cursor.execute(query, tuple(params))
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
                query = f"""INSERT INTO votes 
                (election_id, candidate_id, voter_id, polling_station_id, ward_id, constituency_id, county_id, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                cursor.execute(query, (election_id, candidate_id, current_user.id, current_user.polling_station_id, current_user.ward_id, current_user.constituency_id, current_user.county_id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def create_partition(self, name, polling_station_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                CREATE TABLE IF NOT EXISTS {name}_{polling_station_id.replace('-', '_')} 
                PARTITION OF {name} FOR VALUES IN ('{polling_station_id}')
                """
                cursor.execute(query)
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False 
    
    def delete_partition(self, name, polling_station_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"DROP TABLE IF EXISTS {name}_{polling_station_id.replace('-', '_')}"
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
                    FROM votes 
                    LEFT JOIN candidates ON candidate_id = candidates.id
                    LEFT JOIN voters ON candidates.voter_id = voters.id
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
    
    def insert_election_type(self, code, name):
        id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{code}-{name}')))
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO elections (id, code, name) VALUES (%s, %s, %s)"
                cursor.execute(query, (id, code, name))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_election_type(self, id, code, name):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE elections SET code = %s, name = %s WHERE id = %s"
                cursor.execute(query, (code, name, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_election_types(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH candidates AS(
                    SELECT election_id, COUNT(*) AS ttl_candidates FROM candidates 
                    GROUP BY election_id
                )
                SELECT id, code, name, ttl_candidates
                FROM elections
                LEFT JOIN candidates ON elections.id = candidates.election_id
                ORDER BY code
                """
                cursor.execute(query)
                data = cursor.fetchall()
                elections = []
                for datum in data:
                    elections.append(Election(datum[0], datum[1], datum[2], datum[3]))
                
                return elections
        except Exception as e:
            print(e)
            return []            
    
    def insert_party(self, name, icon):
        id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{name}')))
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO parties (id, name, icon) VALUES (%s, %s, %s)"
                cursor.execute(query, (id, name, icon))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_party(self, id, name, icon):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE parties SET name = %s, icon = %s WHERE id = %s"
                cursor.execute(query, (name, icon, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def delete_party(self, id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"DELETE FROM parties WHERE id = %s"
                cursor.execute(query, (id,))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
        
    def get_parties(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH candidates AS(
                    SELECT party_id, COUNT(*) AS ttl_candidates FROM candidates 
                    GROUP BY party_id
                )
                SELECT id, name, icon, ttl_candidates
                FROM parties
                LEFT JOIN candidates ON parties.id = candidates.party_id
                ORDER BY parties.name
                """
                params = []
                if page>0:
                    query = f"{query} LIMIT 50 OFFSET %s"
                    params.append((page - 1)*50)
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                parties = []
                for datum in data:
                    parties.append(Party(datum[0], datum[1], datum[2], datum[3]))
                
                return parties
        except Exception as e:
            print(e)
            return []            
    
    def insert_candidate(self, id, voter_id, party_id, election_id, icon):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO candidates (id, voter_id, party_id, election_id, icon) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (id, voter_id, party_id, election_id, icon))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def update_candidate(self, id, party_id, election_id, icon):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE candidates SET party_id = %s, election_id = %s, icon = %s WHERE id = %s"
                cursor.execute(query, (party_id, election_id, icon, id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def delete_candidate(self, id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"DELETE FROM candidates WHERE id = %s"
                cursor.execute(query, (id,))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_candidates(self, polling_station_id=None, ward_id=None, constituency_id=None, county_id=None, page=0):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                SELECT candidates.id, v.id_number, CONCAT(v.first_name,' ',v.last_name,' ',v.other_name) AS name, v.phone, candidates.icon,
                polling_stations.name AS polling_station_name, wards.name AS ward_name,constituencies.name AS constituencies_name, counties.name AS county_name,
                election_id, elections.name AS election_name, party_id, parties.name AS party_name, parties.icon AS party_icon, 
                CONCAT(v2.first_name,' ',v2.last_name,' ',v2.other_name) AS running_mate_name, running_mate_icon
                FROM candidates
                JOIN voters v ON voter_id = v.id
                JOIN polling_stations ON polling_station_id = polling_stations.id 
                JOIN wards ON ward_id = wards.id   
                JOIN constituencies ON constituency_id = constituencies.id
                JOIN counties ON county_id = counties.id
                JOIN elections ON election_id = elections.id
                JOIN parties ON party_id = parties.id
                LEFT JOIN voters v2 ON running_mate_voter_id = v2.id
                WHERE 1=1       
                """
                params = []
                if polling_station_id is not None:
                    query = f"{query} AND polling_station_id = %s"
                    params.append(polling_station_id)
                if ward_id is not None:
                    query = f"{query} AND ward_id = %s"
                    params.append(ward_id)
                if constituency_id is not None:
                    query = f"{query} AND constituency_id = %s"
                    params.append(constituency_id)
                if county_id is not None:
                    query = f"{query} AND county_id = %s"
                    params.append(county_id)
                query = f"{query} ORDER BY id_number"
                if page>0:
                    query = f"{query} LIMIT 50 OFFSET %s"
                    params.append((page - 1)*50)
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                candidates = []
                for datum in data:
                    candidates.append(Candidate(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8], datum[9], datum[10], datum[11], datum[12], datum[13], datum[14], datum[15]))
                                    
                return candidates
        except Exception as e:
            print(e)
            return []
    
    def get_registered_voters(self, polling_station_id=None, ward_id=None, constituency_id=None, county_id=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""SELECT COUNT(*)
                FROM voters
                JOIN polling_stations ON polling_station_id = polling_stations.id 
                JOIN wards ON ward_id = wards.id   
                JOIN constituencies ON constituency_id = constituencies.id
                WHERE 1=1      
                """
                params = []
                if polling_station_id is not None:
                    query = f"{query} AND polling_station_id = %s"
                    params.append(polling_station_id)
                if ward_id is not None:
                    query = f"{query} AND ward_id = %s"
                    params.append(ward_id)
                if constituency_id is not None:
                    query = f"{query} AND constituency_id = %s"
                    params.append(constituency_id)
                if county_id is not None:
                    query = f"{query} AND county_id = %s"
                    params.append(county_id)
                
                cursor.execute(query, params)
                data = cursor.fetchone()
                if data:
                    return data[0]
                else:
                    return 0
        except Exception as e:
            print(e)
            return 0