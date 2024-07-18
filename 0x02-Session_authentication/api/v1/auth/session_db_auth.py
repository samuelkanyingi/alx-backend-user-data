#!/usr/bin/env python3
"""SessionDBAuth module"""

from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth
from models import storage


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Create a session and store it in the database"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the user ID based on the session ID from the database"""
        if session_id is None:
            return None
        user_sessions = storage.all(UserSession)
        for user_session in user_sessions.values():
            if user_session.session_id == session_id:
                if self.session_duration <= 0:
                    return user_session.user_id
                if user_session.created_at is None:
                    return None
                if user_session.created_at + timedelta(seconds=self.session_duration) < datetime.now():
                    return None
                return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the session ID from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_sessions = storage.all(UserSession)
        for key, user_session in user_sessions.items():
            if user_session.session_id == session_id:
                storage.delete(user_session)
                storage.save()
                return True
        return False
