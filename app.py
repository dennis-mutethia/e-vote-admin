import os, random
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request, jsonify 


from utils.db import Db
from utils.dashboard import Dashboard
from utils.counties import Counties
from utils.constituencies import Constituencies
from utils.wards import Wards
from utils.polling_stations import PollingStations
from utils.voters_register import VotersRegister
from utils.candidates import Candidates
from utils.election_types import ElectionTypes
from utils.parties import Parties

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

db = Db()

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    return Dashboard(db)() 

@app.route('/counties', methods=['GET', 'POST'])
def counties(): 
    return Counties(db)() 

@app.route('/constituencies', methods=['GET', 'POST'])
def constituencies(): 
    return Constituencies(db)() 

@app.route('/wards', methods=['GET', 'POST'])
def wards(): 
    return Wards(db)() 

@app.route('/polling-stations', methods=['GET', 'POST'])
def polling_stations(): 
    return PollingStations(db)() 

@app.route('/voters-register', methods=['GET', 'POST'])
def voters_register(): 
    return VotersRegister(db)() 

@app.route('/candidates', methods=['GET', 'POST'])
def candidates(): 
    return Candidates(db)() 

@app.route('/election-types', methods=['GET', 'POST'])
def election_types(): 
    return ElectionTypes(db)() 

@app.route('/parties', methods=['GET', 'POST'])
def parties(): 
    return Parties(db)() 

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)