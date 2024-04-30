# routes/main_route.py
from flask import render_template
from flaskpost import app

@app.route('/')
def index():
    return render_template('index.html')
