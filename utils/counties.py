import uuid
from flask import request, render_template

class Counties():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            code = request.form['CountyCode']
            name = request.form['CountyName']
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{int(code)}')))
            if self.db.insert_county(id, code, name.upper()):
                success=f'{name} County Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving {name} County.'
            return success, error
        except Exception as e:
            return None, e
            
    def edit(self):      
        try:
            id = request.form['editCountyId']
            code = request.form['CountyCode']
            name = request.form['CountyName']
            if self.db.update_county(id, code, name.upper()):
                success=f'{name} County Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name} County.'
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
            
        counties = self.db.get_counties()  
        return render_template('counties.html', counties=counties, success=success, error=error, 
                               menu='electoral_units', page='counties')