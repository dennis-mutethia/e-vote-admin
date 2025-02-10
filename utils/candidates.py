import uuid
from flask import request, render_template

class Candidates():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:    
            voter_id = request.form['candidateVoterId']
            party_id = request.form['CandidatePartyId'] 
            election_id = request.form['CandidateElectionId']
            icon = request.form['CandidateIcon']
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{voter_id}-{party_id}-{election_id}')))
            if self.db.insert_candidate(id, voter_id, party_id, election_id, icon):
                success=f'Candidate Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving Candidate.'
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
        voter = None
        if request.method == 'POST':
            if request.form['action'] == 'search':
                id_number = request.form['VoterIdNumber']
                voter = self.db.get_voter(id_number=id_number)
                                
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
        candidates = self.db.get_candidates(station_id, ward_id, constituency_id, county_id)
        parties = self.db.get_parties()
        elections = self.db.get_election_types()
        return render_template('candidates.html', voter=voter, counties=counties, county_id=county_id, constituencies=constituencies, constituency_id=constituency_id, wards=wards, ward_id=ward_id, polling_stations=polling_stations, station_id=station_id, candidates=candidates, 
                               parties=parties, elections=elections, success=success, error=error, menu='elections', page='candidates')