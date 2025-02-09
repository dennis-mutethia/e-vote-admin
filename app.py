import os, random
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request, jsonify 

from utils.counties import Counties
from utils.dashboard import Dashboard
from utils.db import Db

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

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)