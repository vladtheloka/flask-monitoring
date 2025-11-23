from typing import Any, Protocol


class SupportsResource(Protocol):
    def get(self, *args: Any, **kwargs: Any) -> Any: 
        raise NotImplementedError
