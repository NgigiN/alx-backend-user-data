#!/usr/bin/env python3
"""Basic  Authentication"""

import email
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64

from models.user import User


class BasicAuth(Auth):
    """Basic Auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Method that returns the Base64 part of the auth
        header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header,
                          str) or not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_bytes = base64.b64decode(base64_authorization_header)
            return decode_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> (str, str):
        """This method returns the user email and password from the decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """This method instatiates a user and returns a user based
        on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        for use in user:
            if use.is_valid_password(user_pwd):
                return use
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_header = self.extract_base64_authorization_header(auth_header)
        if b64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(b64_header)
        if decoded_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_header)
        if user_credentials is None:
            return None
        user = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        return user
