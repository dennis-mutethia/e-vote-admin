import uuid
from flask import request, render_template

class Dashboard():
    def __init__(self, db):
        self.db = db
        
    def __call__(self):
        id = uuid.uuid5(uuid.NAMESPACE_DNS, ('50298d17-4289-563b-a37c-29019ffbe682'))
        #print(id)
        success = None
        error = None
        if request.method == 'POST':
            if request.form['action'] == 'vote':
                #success, error = self.vote()
                pass
        
        registered_voters = self.db.get_registered_voters(polling_station_id=None, ward_id=None, constituency_id=None, county_id=None)    
        return render_template('dashboard.html', registered_voters=registered_voters,
                               success=success, error=error, menu='dashboard')
