#!/usr/bin/env python3
""" Session Auth views"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login/', strict_slashes=False, methods=["POST"])
def login_session():
    """Authetication for login"""
    mail = request.form.get('email')
    psswd = request.form.get('password')
    if mail is None or len(mail) == 0:
        return jsonify({ "error": "email missing" }), 400
    if psswd is None or len(psswd) == 0:
        return jsonify({ "error": "password missing" }), 400

    user = User.search({"email": mail})
    if user is None or len(user) == 0:
        return jsonify(
                { "error": "no user found for this email" }
                ), 404
    elif not user[0].is_valid_password(psswd):
        return jsonify({ "error": "wrong password" }), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user[0].id)
        user_obj = user[0].to_json()
        user_json = jsonify(user_obj)
        print(f'cookie name: {auth.session_cookie_name} and id: {user_obj["id"]}')
        resp = make_response(user_json)
        resp.set_cookie(auth.session_cookie_name, str(user_obj['id']))
        cook = request.cookies
        print(f'cook: {len(cook)}')
        print(resp)
        for k,v in cook.items():
            print(f'key: {k}, value: {v}')
        return user_json
