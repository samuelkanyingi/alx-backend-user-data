#!/usr/bin/env python3
""" module for auth class """
from typing import List, TypeVar
from flask import request


class Auth:
    """ authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required for a given path. """
        # Placeholder logic for demonstration
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method to retrieve authorization header from request. """
        # Placeholder logic for demonstration
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to retrieve current user from request. """
        # Placeholder logic for demonstration
        return None


    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user email and password from the Base64 decoded value """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
