#!/usr/bin/python3

from flask import Blueprint, request, render_template, flash, url_for, redirect, session
from . import database as db
from .models import User, SensorData
from sqlalchemy import exc
from .config import USRNAME_MIN_LEN, USRNAME_MAX_LEN, MIN_PASSWD_LEN, DISALLOWED_PASSWORD_LIST_PATH, HASH_COST, API_KEY, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import json
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Hash import SHA256
from base64 import b64encode
from werkzeug.exceptions import BadRequestKeyError
import datetime

views = Blueprint("views", __name__)

@views.route("/", methods = ["GET"])
def index():
    ''' Default landing page. Display air quality data. '''

    username = None

    # Used for plotting.
    a013_aqi_values = []
    a055_aqi_values = []
    best_room = ""

    # Check if a user is logged in.
    if "user-id" in session:
        user = User.query.filter_by(uuid = session["user-id"]).first()

        # User deleted, log it out as well.
        if user is None:
            return redirect(url_for("views.logout"))

        # Get current username.
        username = user.username

        # Get entries for the last 24 hours.
        time_window = datetime.datetime.utcnow() - datetime.timedelta(hours = 24)

        # Retrieve sensor data from the database within the time window.
        a013_data = SensorData.query.filter_by(location = "A013").filter(SensorData.time > time_window).all()
        a055_data = SensorData.query.filter_by(location = "A055").filter(SensorData.time > time_window).all()

        if (a013_data is not None) and (a055_data is not None):

            for point in a013_data:
                a013_aqi_values.append((point.id, point.aqi))

            for point in a055_data:
                a055_aqi_values.append((point.id, point.aqi))

            try:
                # Get the name of the best room.
                if a013_data[-1].aqi < a055_data[-1].aqi:
                    best_room = "A013"
                else:
                    best_room = "A055"
            except IndexError:
                best_room = "NO DATA!"

    context = {
        "username": username,
        "a013_aqi_values": a013_aqi_values,
        "a055_aqi_values": a055_aqi_values,
        "best_room": best_room,
    }

    return render_template("index.html", context = context)

@views.route("/register", methods = ["GET", "POST"])
def register():
    ''' User registration page. '''

    REGISTER_TEMPLATE = "register.html"

    if request.method == "POST":

        try:
            # Get user input from form.
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm-password"]
        except BadRequestKeyError:
            flash("Invalid form!", "error")
            return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST

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
                        flash("Password is too common!", "error")
                        return render_template(REGISTER_TEMPLATE), HTTP_400_BAD_REQUEST

        except FileNotFoundError:
            pass
        
        try:
            # Hash the password using bcrypt. Accept all password lengths.
            length_insensitive_password = b64encode(SHA256.new(password.encode()).digest())
            bcrypt_password_hash = bcrypt(length_insensitive_password, HASH_COST)
        except ValueError:
            flash("Invalid password!", "error")
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

    LOGIN_TEMPLATE = "login.html"
    ERROR_MSG = "Incorrect username or password!"

    if request.method == "POST":

        try:
            # Get user input from form.
            username = request.form["username"]
            password = request.form["password"]
        except BadRequestKeyError:
            flash("Invalid form!", "error")
            return render_template(LOGIN_TEMPLATE), HTTP_400_BAD_REQUEST

        # Retrieve the user, or None if non-existent.
        user = User.query.filter_by(username = username).first()

        # Check if the username exists in the database.
        if user is None:
            flash(ERROR_MSG, "error")
            return render_template(LOGIN_TEMPLATE), HTTP_400_BAD_REQUEST

        try:
            # Validate the password of the retrieved user.
            length_insensitive_password = b64encode(SHA256.new(password.encode()).digest())
            bcrypt_check(length_insensitive_password, user.password_hash)
        except ValueError:
            flash(ERROR_MSG, "error")
            return render_template(LOGIN_TEMPLATE), HTTP_400_BAD_REQUEST

        # Success, set user session.
        session['user-id'] = user.uuid

        # Set user as active.
        if user.activated != True:
            user.activated = True
            db.session.commit()

        flash(f"Logged in as: {user.username}", "success")
        return redirect(url_for("views.index"))

    # Present log in form on a GET request.
    return render_template("login.html")

@views.route("/logout", methods = ["GET"])
def logout():
    ''' Log out the user. '''

    # Remove user from session if it exists.
    session.pop('user-id', None)
    return redirect(url_for("views.login"))

@views.route("/api/sensors/submit-bme680-sensor-data", methods=["POST"])
def submit_bme680_sensor_data():
    ''' Store sensor data for a Bosch BME680 sensor. '''

    SUCCESS_CODE = 201
    UNAUTHORIZED = 401

    # Expect JSON data only.
    data = request.get_json()
    if data is None:
        return "", HTTP_400_BAD_REQUEST

    try:
        # Get data from the sensor.
        api_key = data["api_key"]
        location = data["location"]
        temperature = data["temperature"]
        pressure = data["pressure"]
        humidity = data["humidity"]
        aqi = data["aqi"]
    except:
        return "", HTTP_400_BAD_REQUEST

    # Validate API key.
    if api_key != API_KEY:
        return "", UNAUTHORIZED

    # Create a new data point.
    data_point = SensorData(
        location = location,
        temperature = temperature,
        pressure = pressure,
        humidity = humidity,
        aqi = aqi,
    )

    try:
        # Store the data.
        db.session.add(data_point)
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        return "", HTTP_400_BAD_REQUEST

    return "", SUCCESS_CODE
