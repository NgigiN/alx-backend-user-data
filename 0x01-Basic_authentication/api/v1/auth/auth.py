#!/usr/bin/env python3
"""A class to manage the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth():
  """Class to manage the Authentication"""

  def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
    """Method for basic authentication"""
    return False

  def authorization_header(self, request=None) -> str:
    """Method handling the authorization header"""
    return None

  def current_user(self, request=None) -> TypeVar('User'):
    """Method for handling users
    """
    return None
