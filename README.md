# Web Authentication:
Assignment four in INF-2310 Computer Security.
## User guide:
- Run the debug server: ``` ./runserver.py ```
- Run the debug server and reset the database: ``` ./runserver.py -r ``` or ``` ./runserver.py --reset ```
- Deploy: follow the ``` deploy.txt ``` guide.
## Requirements:
The server should display a greeting message to authenticated users.
In addition the following requirements must be achieved:
- User credentials must be stored in a persistent file on disk.
- Protection against network-based replay attacks and network snooping.
- Stored passwords must be resilient to dictionary attacks.
- Log authentication requests (*OPT).
## Endpoints:
- "/" (GET) - welcome message, username of a logged-in user, a link to the register and login page.
- "/register" (GET, POST) - form for adding new users, username and password w. verification + errors.
- "/login" (GET, POST) - username, password and redirect to "/" on successful login.
All API endpoints should return HTML documents.
### Error messages:
- Username is already taken.
- Password verification fails.
- Password is of insufficient strength.
### Frameworks:
- Python 3.
- Flask.
- Bcrypt.
- OpenSSL + Let's Encrypt.
### Sources:
- [Flask](https://flask.palletsprojects.com/en/2.2.x/).
- [Secure Password Hashing](https://security.blogoverflow.com/2013/09/about-secure-password-hashing/).
- [pyCryptoDome](https://pycryptodome.readthedocs.io/en/latest/).
- [Flash w. Flask](https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/).
- [PwnedPasswordsTop100k](https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json).
- [Bcrypt Docs](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html).
- [Sessions in Flask](https://pythonbasics.org/flask-sessions/).
- [View Decorators](https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/).
