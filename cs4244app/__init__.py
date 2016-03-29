from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from cs4244app.expertapp.controller import expertapp
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)


app.register_blueprint(expertapp, url_prefix='/expertapp')


@app.route('/')
def mainSite():
    return render_template('mainindex.html')