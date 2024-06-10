#!/usr/bin/env python3
"""A class to manage the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Class to manage the Authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method for basic authentication"""
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_paths = path.rstrip('/') + '/'
        normalized_excluded_paths = [
            ep.rstrip('/') + '/' for ep in excluded_paths]

        if normalized_paths in normalized_excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Method handling the authorization header"""
        if request is None:
            return None
        header_value = request.headers.get('Authorization')
        if header_value is None:
            return None

        return header_value

    def current_user(self, request=None) -> TypeVar('User'):
        """Method for handling users"""
        return None
