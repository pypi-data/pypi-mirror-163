"""
.. code-block:: python

    from aioauth import requests

Request objects used throughout the project.

----
"""
from dataclasses import dataclass
from typing import Any, Optional

from .collections import HTTPHeaderDict
from .config import Settings
from .types import CodeChallengeMethod, GrantType, RequestMethod, ResponseMode


@dataclass
class Query:
    """
    Object that contains a client's query string portion of a request.
    Read more on query strings `here <https://en.wikipedia.org/wiki/Query_string>`__.
    """

    client_id: Optional[str] = None
    redirect_uri: str = ""
    response_type: Optional[str] = None
    state: str = ""
    scope: str = ""
    nonce: Optional[str] = None
    code_challenge_method: Optional[CodeChallengeMethod] = None
    code_challenge: Optional[str] = None
    response_mode: Optional[ResponseMode] = None


@dataclass
class Post:
    """
    Object that contains a client's post request portion of a request.
    Read more on post requests `here <https://en.wikipedia.org/wiki/POST_(HTTP)>`__.
    """

    grant_type: Optional[GrantType] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    code: Optional[str] = None
    token: Optional[str] = None
    token_type_hint: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class Request:
    """Object that contains a client's complete request."""

    method: RequestMethod
    headers: HTTPHeaderDict = HTTPHeaderDict()
    query: Query = Query()
    post: Post = Post()
    url: str = ""
    user: Optional[Any] = None
    settings: Settings = Settings()
