from flask import render_template
from . import main

@main.get("/")
def landing():
    return render_template("main/landing.html")