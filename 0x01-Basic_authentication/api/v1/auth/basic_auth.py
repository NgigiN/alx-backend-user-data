#!/usr/bin/env python3
"""Basic  Authentication"""

import email
from api.v1.auth.auth import Auth
import base64


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
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        decoded_bytes = base64.b64decode(decoded_base64_authorization_header)
        decoded_str = decoded_bytes.decode('utf-8')

        if ":" not in decoded_str:
            return None, None
        email, password = decoded_str.split(':', 1)

        return email, password
