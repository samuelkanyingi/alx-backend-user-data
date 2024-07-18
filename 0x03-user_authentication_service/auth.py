#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def _generate_uuid() -> str:
        """Generates a new UUID and returns its string representation."""
        return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created user object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user is found, proceed with registration
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user and returns the session ID."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: Optional[str]) -> Optional[User]:
        """Returns the user corresponding to the session ID."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session by updating the user's session ID to None."""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
        except ValueError:
            # If the user does not exist, raise a ValueError
            #raise ValueError(f"User with email {email} does not exist")
            raise ValueError("User not found")

        # Generate a new UUID
        reset_token = str(uuid.uuid4())

        # Update the user's reset_token in the database
        self._db.update_user(user.id, reset_token=reset_token)

        # Return the reset token
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password using the reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)


if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))
