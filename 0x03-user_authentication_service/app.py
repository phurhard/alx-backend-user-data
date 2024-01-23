#!/usr/bin/env python3
"""API documentation"""
from flask import Flask, jsonify, request, abort
from flask import make_response, url_for, redirect
from auth import Auth
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
AUTH = Auth()


@app.route('/')
def status():
    '''Returns Greetings'''
    return jsonify({
        "message": "Bienvenue"
    })


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    '''A POST request function that creates a new user'''
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    '''Logins a user in using the session storage kept by the machine server'''
    if request.form:
        mail = request.form.get("email")
        pwd = request.form.get("password")
        if AUTH.valid_login(mail, pwd):
            session = AUTH.create_session(mail)
            resp = make_response(jsonify({"email": mail,
                                          "message": "logged in"}), 200)
            resp.set_cookie('session_id', str(session))
            return resp
        else:
            abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    '''Delete a users session from the list of logged in users'''
    session = request.cookies.get('session_id')
    if session is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('/')), 302  # Redirection to GET /
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    '''User profile'''
    try:
        session = request.cookies.get("session_id")
        if session is None:
            abort(403)
        user = AUTH.get_user_from_session_id(session)
        if user is not None:
            return jsonify({"email": user.email,
                            "session": user.session_id}), 200
        else:
            abort(403)
    except Exception as e:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    '''Generates and sends the token for a new password'''
    try:
        mail = request.form.get("email")
        user_token = AUTH.get_reset_password_token(mail)
        return jsonify({"email": mail, "reset_token": user_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    '''Uses the update password from AUTH to update the password
    this is the route logic'''
    mail = request.form.get("email")
    newPwd = request.form.get("new_password")
    reset_token = request.form.get("reset_token")
    try:
        AUTH.update_password(reset_token, newPwd)
        return jsonify({"email": mail, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
