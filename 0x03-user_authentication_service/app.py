#!/usr/bin/env python3
"""API documentation"""
from flask import Flask, jsonify, request
from auth import Auth
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"*": {"origins": "*"}})
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
        return jsonify({"email": email, "massage": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
