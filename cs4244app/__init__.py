from flask import Flask, render_template, redirect, url_for
from expertapp.controller import expertapp
import os

app = Flask(__name__)



app.register_blueprint(expertapp, url_prefix='/expertapp')


@app.route('/')
def mainSite():
    return redirect(url_for('expertapp.index'))