from flask import Flask, request
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)

# Digest Auth requires a secret key to generate secure "nonces"
app.config['SECRET_KEY'] = 'your-super-secret-key-here'

# Initialize the Digest Auth object
auth = HTTPDigestAuth()

# Your database of users
users = {
    "hrm": "h"
}

# Instead of checking the password yourself, you give the library a way 
# to look up the password. The library will do all the MD5 math for you!
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route("/")
def home():
    return "<h1> Hi How Are you </h2> <a href=\"/dashboard\"> Dashboard Page </a>"

# Use the @auth.login_required decorator instead of your custom one
@app.route("/dashboard")
@auth.login_required
def dashboard():
    # You can access the logged-in user via auth.current_user()
    return f"<h1> It's Dashboard. Welcome, {auth.current_user()}! </h2> <a href=\"/profile\"> Profile Page </a>"

@app.route("/profile")
@auth.login_required
def profile():
    return "<h2> Your Profile is Amazing </h2> <a href=\"/dashboard\"> Dashboard Page </a>"

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
