from flask import Flask, request, make_response
from functools import wraps

app = Flask(__name__)

def basic_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.authorization
        if auth:
            if auth.username == "hrm" and auth.password == "h":
                    return f(*args, **kwargs)

        return make_response(
            "You Must Login, You are not Logged In.",
            401,
            {'WWW-AUTHENTICATE': 'Basic realm="Login Required"'}
        )
    return decorator
        

@app.route("/")
def home():
    return "<h1> Hi How Are you </h2> <a href=\"/dashboard\"> Dashboard Page </a>"


@app.route("/dashboard")
@basic_auth
def dashboard():
    return "<h1> It's Dashboard </h2> <a href=\"/profile\"> Profile Page </a>"

@app.route("/profile")
@basic_auth
def profile():
    return "<h2> Your Profile is Amazing </h2> <a href=\"/dashboard\"> Dashboard Page </a>"

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
