#!/usr/bin/env python3
""" SessionAuth module
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth class that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        Args:
            user_id (str): The user ID to create a session for.
        Returns:
            str: The Session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
