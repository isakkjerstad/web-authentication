# Web Authentication:
Assignment four in INF-2310 Computer Security.
## Requirements:
The server should display a greeting message to authenticated users.
In addition the following requirements must be achieved:
- User credentials must be stored in a persistent file on disk.
- Protection against network-based replay attacks and network snooping.
- Stored passwords must be resilient to dictionary attacks.
- Log authentication requests.
## Endpoints:
- "/" (GET) - welcome message, username of a logged-in user, a link to the register and login page.
- "/register" (GET, PUT) - form for adding new users, username and password w. verification + errors.
- "/login" (GET, PUT) - username, password and redirect to "/" on successful login.
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


