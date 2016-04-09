from flask import Flask, render_template
from expertapp.controller import expertapp
import os

app = Flask(__name__)



app.register_blueprint(expertapp, url_prefix='/expertapp')


@app.route('/')
def mainSite():
    return render_template('mainindex.html')