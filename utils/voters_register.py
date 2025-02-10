import uuid
from flask import request, render_template

class VotersRegister():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:            
            id_number = request.form['VoterIdNumber']
            first_name = request.form['VoterFirstName'] 
            last_name = request.form['VoterLastName']
            other_name = request.form['VoterOtherName']
            phone = request.form['VoterPhone'] 
            polling_station_id = request.form['VoterPollingStationId']
            fingerprint_hash = ''
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{id_number}-{polling_station_id}-{phone}')))
            if self.db.insert_voter(id, id_number, first_name.upper(), last_name.upper(), other_name.upper(), phone, polling_station_id, fingerprint_hash):
                success=f'{first_name} {last_name} Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving {first_name} {last_name}.'
            return success, error
        except Exception as e:
            return None, e
            
    def edit(self):  
        try:
            id = request.form['editVoterId']
            id_number = request.form['VoterIdNumber']
            first_name = request.form['VoterFirstName'] 
            last_name = request.form['VoterLastName']
            other_name = request.form['VoterOtherName']
            phone = request.form['VoterPhone'] 
            polling_station_id = request.form['VoterPollingStationId']
            fingerprint_hash = ''
            if self.db.update_voter(id, id_number, first_name.upper(), last_name.upper(), other_name.upper(), phone, polling_station_id, fingerprint_hash):
                success=f'{first_name} {last_name} Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {first_name} {last_name}.'
            return success, error
        except Exception as e:
            return None, e
            
    def delete(self):  
        try:
            id = request.form['removeVoterId']
            if self.db.delete_polling_station(id):
                success=f'Voter Deleted Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while deleting Voter.'
            return success, error
        except Exception as e:
            return None, e
           
    def __call__(self):
        success = None
        error = None
        if request.method == 'POST':
            if request.form['action'] == 'add':
                success, error = self.add()
            if request.form['action'] == 'edit':
                success, error = self.edit()
            if request.form['action'] == 'remove':
                success, error = self.delete()
                
        county_id = request.args.get('county') or None
        counties = self.db.get_counties()
        constituency_id = request.args.get('constituency') or None
        constituencies = self.db.get_constituencies(county_id)
        wards = self.db.get_wards(constituency_id) 
        ward_id = request.args.get('ward') or None
        polling_stations = self.db.get_polling_stations(ward_id, constituency_id, county_id)  
        station_id = request.args.get('station') or None
        voters = self.db.get_voters(station_id, ward_id, constituency_id, county_id)
        return render_template('voters-register.html', counties=counties, county_id=county_id, constituencies=constituencies, constituency_id=constituency_id, wards=wards, ward_id=ward_id, polling_stations=polling_stations, station_id=station_id, voters=voters, success=success, error=error, 
                               menu='voters_register')