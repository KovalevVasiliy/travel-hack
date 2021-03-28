from typing import Any, Dict, Protocol


class HasID(Protocol):
    id: Any


AnyDict = Dict[str, Any]
