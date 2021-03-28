from contextvars import ContextVar
from typing import Any, Dict, Optional
from uuid import uuid4

data: ContextVar[Optional[Dict]] = ContextVar('data', default=None)


class CurrentContext:
    def get(self, key: str) -> Any:
        data_dict = data.get()
        if not data_dict:
            return None
        return data_dict.get(key)

    def set(self, key: str, value: Any) -> None:
        data_dict = data.get()
        if not data_dict:
            data_dict = {}
            data.set(data_dict)
        data_dict[key] = value

    def init(self) -> None:
        self.set_request_id(uuid4().hex)

    def set_actor(self, actor_type: str, actor_id: str) -> None:
        self.set('actor_type', actor_type)
        self.set('actor_id', actor_id)

    def set_request_id(self, request_id: str) -> None:
        self.set('request_id', request_id)

    def get_request_id(self) -> Optional[str]:
        return self.get('request_id')

    def get_actor_id(self) -> Optional[str]:
        return self.get('actor_id')

    def get_actor_type(self) -> Optional[str]:
        return self.get('actor_type')


current_context = CurrentContext()
