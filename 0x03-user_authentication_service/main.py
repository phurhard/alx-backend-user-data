#!/usr/bin/env python3
"""A test for the user authentication
Run this file to validate how the user authentication works"""
import requests
# Testing


def register_user(email: str, password: str) -> None:
    """Creates a new user on the db

    Keyword arguments:
    email -- email to use to register the user
    Return: Returns a 200 status code and a message
            that user has been created successfully
    """

    url = "http://127.0.0.1:5000/users"
    message: dict[str, str] = {
        "email": email,
        "message": "user created"
        }
    user: requests.Response = requests.post(url,
                                            data={"email": email,
                                                  "password": password})
    assert (user.status_code == 200)
    assert (user.json() == message)


def log_in_wrong_password(email: str, password: str) -> None:
    """Users logs in with wrong password
    Raises an error

    Keyword arguments:
    email -- Email of user used to register
    password --- Password passed which is incorrect
    Return: returns a 401 code which means unauthorized
    """

    url = "http://127.0.0.1:5000/sessions"
    user = requests.post(url, data={"email":  email, "password": password})
    assert (user.status_code == 401)


def profile_unlogged() -> None:
    """The profile of the user is not activated cause
    there is no session id gotten

    Keyword arguments:
    argument -- description
    Return: Raises a 403 Error
    """
    url = "http://127.0.0.1:5000/profile"
    user = requests.get(url)
    assert (user.status_code == 403)


def log_in(email: str, password: str) -> str:
    """Log in with the correct password

    Keyword arguments:
    email -- Email used to register
    password -- Password used to register
    Return: Returns a message that user is logged in
    """
    url = "http://127.0.0.1:5000/sessions"
    message = {"email": email, "message": "logged in"}
    user = requests.post(url, data={"email": email, "password": password})
    assert (user.status_code == 200)
    assert (user.json() == message)
    return user.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """User profile is provided since there is a session id

    Keyword arguments:
    session_id -- ID used to identify the user at the timestamp
    Return: 200 status code, and a message user mail
    """
    url = "http://127.0.0.1:5000/profile"
    cookie = {"session_id": session_id}
    user = requests.get(url, cookies=cookie)
    assert (user.status_code == 200)


def log_out(session_id: str) -> None:
    """Given a session id, deleete the user session
    thereby logging the user out

    Keyword arguments:
    session_id -The session id of the user
    Return: Returns Nothing
    """
    url = "http://127.0.0.1:5000/sessions"
    cookie = {"session_id": session_id}
    user = requests.delete(url, cookies=cookie)
    assert (user.status_code == 200)


def reset_password_token(email: str) -> str:
    """Get a new token to create a new password

    Keyword arguments:
    email -- Email of usser
    Return: Returns the reseet token
    """
    url = "http://127.0.0.1:5000/reset_password"
    user = requests.post(url, data={"email": email})
    assert (user.status_code == 200)
    return user.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Takes the reset token and sets a new password for the user

    Keyword arguments:
    Email -- The user email
    newPassword -- The user new password
    reset_token -- The reset token generated for the user
    Return: Returns nothinng other than a confirmation the
            password has been updated
    """
    url = "http://127.0.0.1:5000/reset_password"
    user = requests.put(url, data={"email": email,
                                   "reset_token": reset_token,
                                   "new_password": new_password})
    assert (user.status_code == 200)


EMAIL = "vuillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
