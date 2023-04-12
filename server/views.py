#!/usr/bin/python3

from flask import Blueprint, request, render_template

views = Blueprint("views", __name__)

@views.route("/", methods = ["GET"])
def index():
    ''' Default landing page. '''

    return render_template("index.html")

@views.route("/register", methods = ["GET", "POST"])
def register():
    ''' User registration page. '''

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

    return render_template("register.html")

@views.route("/login", methods = ["GET", "POST"])
def login():
    ''' User login page. '''

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

    return render_template("login.html")
