from flask import request, render_template

class Constituencies():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            code = request.form['ConstituencyCode']
            county_id = request.form['CountyId']
            name = request.form['ConstituencyName']
            if self.db.insert_constituency(code, county_id, name.upper()):
                success=f'{name} Constituency Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving {name} Constituency.'
            return success, error
        except Exception as e:
            return None, e
            
    def edit(self):      
        try:
            id = request.form['editConstituencyId']
            code = request.form['ConstituencyCode']
            county_id = request.form['CountyId']
            name = request.form['ConstituencyName']
            if self.db.update_constituency(id, code, county_id, name.upper()):
                success=f'{name} Constituency Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name} Constituency.'
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
        constituencies = self.db.get_constituencies(county_id)  
        return render_template('constituencies.html', counties=counties, county_id=county_id, constituencies=constituencies, success=success, error=error, 
                               menu='electoral_units', page='constituencies')