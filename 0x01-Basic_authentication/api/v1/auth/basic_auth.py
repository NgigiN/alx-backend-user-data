#!/usr/bin/env python3
"""Basic  Authentication"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Auth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Method that returns the Base64 part of the auth
        header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str) or not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
