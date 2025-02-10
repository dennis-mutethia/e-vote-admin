import uuid
from flask import request, render_template

class PollingStations():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            code = request.form['PollingStationCode']
            ward_id = request.form['WardId'] 
            name = request.form['PollingStationName']
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{code}-{ward_id}-{name}')))
            if self.db.insert_polling_station(id, code, ward_id, name.upper()):
                self.db.create_partition('voters', id)
                self.db.create_partition('votes', id)
                self.db.create_partition('sms_codes', id)
                success=f'{name} Polling Station Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving {name} PollingStation.'
            return success, error
        except Exception as e:
            return None, e
            
    def edit(self):  
        try:
            id = request.form['editPollingStationId']
            code = request.form['PollingStationCode']
            ward_id = request.form['WardId'] 
            name = request.form['PollingStationName']
            if self.db.update_polling_station(id, code, ward_id, name.upper()):
                self.db.create_partition('voters', id)
                self.db.create_partition('votes', id)
                self.db.create_partition('sms_codes', id)
                success=f'{name} PollingStation Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name} PollingStation.'
            return success, error
        except Exception as e:
            return None, e
            
    def delete(self):  
        try:
            id = request.form['removePollingStationId']
            if self.db.delete_polling_station(id):
                self.db.delete_partition('voters', id)
                self.db.delete_partition('votes', id)
                self.db.delete_partition('sms_codes', id)
                success=f'PollingStation Deleted Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while deleting PollingStation.'
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
        return render_template('polling-stations.html', counties=counties, county_id=county_id, constituencies=constituencies, constituency_id=constituency_id, wards=wards, ward_id=ward_id, polling_stations=polling_stations, success=success, error=error, 
                               menu='electoral_units', page='polling_stations')