import os
from flask import request, render_template
from werkzeug.utils import secure_filename

class Parties():
    def __init__(self, db):
        self.db = db
            
    def add(self):      
        try:
            name = request.form['PartyName']
            icon = request.files['PartyIcon']
            filename = secure_filename(icon.filename)
            icon.save(os.path.join('static/assets/img/parties/', filename))
            if self.db.insert_party(name.upper(), filename):
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
            id = request.form['editPartyId']
            name = request.form['PartyName']
            icon = request.files['PartyIcon']
            filename = secure_filename(icon.filename)
            icon.save(os.path.join('static/assets/img/parties/', filename))
            if self.db.update_party(id, name.upper(), filename):
                success=f'{name} Updated Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while updating {name}.'
            return success, error
        except Exception as e:
            return None, e
            
    def delete(self):      
        try:
            id = request.form['removePartyId']
            if self.db.delete_party(id):
                success=f'Political Party Deleted Successful.'
                error=None
            else:
                success=None
                error=f'An error occurred while deleting Political Party'
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
            
        parties = self.db.get_parties()
        return render_template('parties.html', parties=parties, success=success, error=error, 
                               menu='elections', page='parties')