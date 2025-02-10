from flask import request, render_template

class ElectionTypes():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            code = request.form['ElectionTypeCode']
            name = request.form['ElectionTypeName']
            if self.db.insert_election_type(code, name.upper()):
                success=f'{name} Saved Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while saving {name}.'
            return success, error
        except Exception as e:
            return None, e
            
    def edit(self):      
        try:
            id = request.form['editElectionTypeId']
            code = request.form['ElectionTypeCode']
            name = request.form['ElectionTypeName']
            if self.db.update_election_type(id, code, name.upper()):
                success=f'{name} Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name}.'
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
            
        election_types = self.db.get_election_types()
        return render_template('election-types.html', election_types=election_types, success=success, error=error, 
                               menu='elections', page='election_types')