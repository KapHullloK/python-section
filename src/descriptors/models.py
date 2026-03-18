from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.path = path

    def __get__(self, instance, owner):
        return self._get_by_path(instance.payload, self.path)

    def __set__(self, instance, value):
        self._set_by_path(instance.payload, self.path, value)

    @classmethod
    def _get_by_path(cls, data: dict, path: str) -> Any:
        keys = path.split('.')
        current = data
        for key in keys:
            current = current.get(key, None)
            if current is None:
                return None
        return current

    @classmethod
    def _set_by_path(cls, data: dict, path: str, value: Any) -> None:
        keys = path.split('.')
        current = data
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        current[keys[-1]] = value
