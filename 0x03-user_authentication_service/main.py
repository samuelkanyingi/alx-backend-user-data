#!/usr/bin/env python3
"""
Main module for testing the user authentication service.
"""
import requests


BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """ validate user registration """
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ validate wrong password """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 402


def log_in(email: str, password: str) -> str:
    """ validate login """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    #assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """ validate profile request with no login """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ validate profile request logged in """
    response = requests.get(f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    response = requests.delete(f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email, "reset_token": reset_token, "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
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
