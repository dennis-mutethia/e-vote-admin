import os, random
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request, jsonify 

#from utils.dashboard import Dashboard
from utils.data import Data 

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

data = Data()

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    return render_template('dashboard.html', registered_voters=0)

@app.route('/counties', methods=['GET', 'POST'])
def counties(): 
    counties = data.get_counties()
    return render_template('counties.html', counties=counties, menu='electoral_units', page='counties')

@app.route('/constituencies', methods=['GET', 'POST'])
def constituencies():
    county_names = sorted(data.get_county_names())
    county_name = request.args.get('county') or None 
    constituencies = data.get_constituencies(county_name)
    return render_template('constituencies.html', county_name=county_name, county_names=county_names, constituencies=constituencies, menu='electoral_units', page='constituencies')

@app.route('/wards', methods=['GET', 'POST'])
def wards(): 
    county_names = sorted(data.get_county_names())
    county_name = request.args.get('county') or None 
    constituency_name = request.args.get('constituency') or None 
    wards, constituency_names = data.get_wards(county_name=county_name, constituency_name=constituency_name)
    return render_template('wards.html', county_name=county_name, county_names=county_names, constituency_names=constituency_names, constituency_name=constituency_name, wards=wards, menu='electoral_units', page='wards')

@app.route('/polling-stations', methods=['GET', 'POST'])
def polling_stations(): 
    county_names = sorted(data.get_county_names())
    county_name = request.args.get('county', county_names[0]) 
    constituency_name = request.args.get('constituency') or None 
    ward_name = request.args.get('ward') or None 
    polling_stations, ward_names, constituency_names = data.get_polling_stations(county_name=county_name, constituency_name=constituency_name, ward_name=ward_name)
    return render_template('polling-stations.html', county_name=county_name, county_names=county_names, constituency_names=constituency_names, constituency_name=constituency_name, 
                           ward_names=ward_names, ward_name=ward_name, polling_stations=polling_stations, menu='electoral_units', page='polling_stations')

@app.route('/voters-register', methods=['GET', 'POST'])
def voters_register():     
    county_names = sorted(data.get_county_names())
    county_name = request.args.get('county', county_names[0]) 
    constituency_name = request.args.get('constituency') or None 
    ward_name = request.args.get('ward') or None 
    polling_station_name = request.args.get('polling_station_name') or None 
    voters, polling_station_name, polling_station_names, ward_names, constituency_names = data.get_voters(county_name=county_name, constituency_name=constituency_name, ward_name=ward_name, polling_station_name=polling_station_name)
    return render_template('voters-register.html', county_name=county_name, county_names=county_names, constituency_names=constituency_names, constituency_name=constituency_name, 
                           ward_names=ward_names, ward_name=ward_name, polling_station_names=polling_station_names, polling_station_name=polling_station_name, voters=voters,
                           menu='voters_register')


@app.route('/candidates', methods=['GET', 'POST'])
def candidates(): 
    data.get_counties()
    return render_template('counties.html', counties=counties, menu='electoral_units', page='counties') 

@app.route('/election-types', methods=['GET', 'POST'])
def election_types(): 
    data.get_counties()
    return render_template('counties.html', counties=counties, menu='electoral_units', page='counties')

@app.route('/parties', methods=['GET', 'POST'])
def parties(): 
    data.get_counties()
    return render_template('counties.html', counties=counties, menu='electoral_units', page='counties')

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)