#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
routes = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
auth = getenv("AUTH_TYPE")
if auth:
    if auth == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before():
    """Runs before any other request
    and runs at each request to the server"""
    if auth is None:
        pass
    elif not auth.require_auth(request.path, routes):
        pass
    elif auth.authorization_header(request) is None:
        abort(401)
    elif auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorised(error) -> str:
    """ Unauthorised error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=1)
