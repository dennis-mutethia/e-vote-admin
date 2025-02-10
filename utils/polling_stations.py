from flask import request, render_template

class PollingStations():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            code = request.form['PollingStationCode']
            ward_id = request.form['WardId'] 
            name = request.form['PollingStationName']
            if self.db.insert_polling_station(code, ward_id, name.upper()):
                success=f'{name} PollingStation Saved Successful.'
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
                success=f'{name} PollingStation Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name} PollingStation.'
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
        
        ward_id = request.args.get('ward') or None
        wards = self.db.get_wards()
        polling_stations = self.db.get_polling_stations(ward_id)  
        return render_template('polling_stations.html', wards=wards, ward_id=ward_id, polling_stations=polling_stations, success=success, error=error, 
                               menu='electoral_units', page='polling_stations')