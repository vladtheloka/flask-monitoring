from typing import Any, Protocol


class SupportsResource(Protocol):
    """
    Protocol for Flask-RESTful resources.
    Helps Pylance understand add_resource().
    """
    def get(self, *args: Any, **kwargs: Any) -> Any: ...