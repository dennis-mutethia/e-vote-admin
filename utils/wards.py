from flask import request, render_template

class Wards():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            code = request.form['WardCode']
            constituency_id = request.form['ConstituencyId'] 
            name = request.form['WardName']
            if self.db.insert_ward(code, constituency_id, name.upper()):
                success=f'{name} Ward Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving {name} Ward.'
            return success, error
        except Exception as e:
            return None, e
            
    def edit(self):      
        try:
            id = request.form['editWardId']
            code = request.form['WardCode']
            constituency_id = request.form['ConstituencyId'] 
            name = request.form['WardName']
            if self.db.update_ward(id, code, constituency_id, name.upper()):
                success=f'{name} Ward Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name} Ward.'
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
        
        county_id = request.args.get('county') or None
        counties = self.db.get_counties()
        constituency_id = request.args.get('constituency') or None
        constituencies = self.db.get_constituencies(county_id)
        wards = self.db.get_wards(constituency_id, county_id)  
        return render_template('wards.html', counties=counties, county_id=county_id, constituencies=constituencies, constituency_id=constituency_id, wards=wards, success=success, error=error, 
                               menu='electoral_units', page='wards')