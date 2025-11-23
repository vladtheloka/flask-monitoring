from __future__ import annotations
from typing import Any, Dict
from flask_restful import Resource as FlaskResource


class Resource(FlaskResource):
    """
    Strongly-typed wrapper around Flask-RESTful Resource.
    Pylance understands its methods and stops warning.
    """

    def get(self) -> Dict[str, Any]:
        raise NotImplementedError

    def post(self) -> Dict[str, Any]:
        raise NotImplementedError

    def put(self) -> Dict[str, Any]:
        raise NotImplementedError

    def delete(self) -> Dict[str, Any]:
        raise NotImplementedError
