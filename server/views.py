#!/usr/bin/python3

from flask import Blueprint, request, render_template, flash, url_for, redirect
from . import database as db
from .models import User
from sqlalchemy import exc
from .config import USRNAME_MIN_LEN, USRNAME_MAX_LEN, MIN_PASSWD_LEN, DISALLOWED_PASSWORD_LIST_PATH, HASH_COST, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import json
from Crypto.Protocol.KDF import bcrypt
from Crypto.Hash import SHA256
from base64 import b64encode

views = Blueprint("views", __name__)

@views.route("/", methods = ["GET"])
def index():
    ''' Default landing page. '''

    # TODO: Display user information + extras!

    return render_template("index.html")

@views.route("/register", methods = ["GET", "POST"])
def register():
    ''' User registration page. '''

    REGISTER_TEMPLATE = "register.html"

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        # Validate username according to the database rules.
        if len(username) < USRNAME_MIN_LEN or len(username) > USRNAME_MAX_LEN:
            flash("Invalid username!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST

        # Validate matching passwords.
        if password != confirm_password:
            flash("Passwords does not match!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST

        # Check the password length.
        if len(password) < MIN_PASSWD_LEN:
            flash(f"Password must be at least {MIN_PASSWD_LEN} characters long!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST
        
        try:
            # Check that the requested password is not a common and pwned password.
            with open(DISALLOWED_PASSWORD_LIST_PATH, "rb") as disallowed_password_file:

                disallowed_passwords = json.load(disallowed_password_file)
                
                for disallowed_password in disallowed_passwords:
                    if password == disallowed_password:
                        flash(f"Password is too common!", "error")
                        return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST

        except FileNotFoundError:
            pass
        
        try:
            # Hash the password using bcrypt. Accept all password lengths.
            length_insensitive_password = b64encode(SHA256.new(password.encode()).digest())
            bcrypt_password_hash = bcrypt(length_insensitive_password, HASH_COST)
        except ValueError:
            flash(f"Invalid password!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST

        # Create the new user to add in the database.
        new_user = User(username = username, password_hash = bcrypt_password_hash)

        try:
            # Attempt to add new user.
            db.session.add(new_user)
            db.session.flush()
        except exc.IntegrityError:
            # Username already taken.
            db.session.rollback()
            flash(f"Username '{username}' is already taken!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST
        except exc.SQLAlchemyError:
            # Catch general database errors.
            db.session.rollback()
            flash("Failed to create a new user, please try again!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_500_INTERNAL_SERVER_ERROR
        else:
            # Success, new user can be added.
            db.session.commit()

        flash("New user created successfully!", "success")
        return redirect(url_for("views.login"))

    # Present registration form on a GET request.
    return render_template("register.html")

@views.route("/login", methods = ["GET", "POST"])
def login():
    ''' User log in page. '''

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # TODO: Implement log in!

    # Present log in form on a GET request.
    return render_template("login.html")
