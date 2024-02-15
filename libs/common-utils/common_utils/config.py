import os
from pathlib import Path
from re import L
import re
from typing import Any, Literal, Self, Union
import yaml

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/config"))
if not CONFIG_PATH.exists():
    raise FileNotFoundError(
        f"No configs found at {CONFIG_PATH}, please set the CONFIG_PATH environment variable"
    )
ENVIROMENT = os.environ.get("ENVIROMENT", "development")
if ENVIROMENT not in ["development", "production"]:
    raise ValueError(
        "ENVIROMENT environment variable should be set to 'development' or 'production'"
    )


class ConfigNode:
    name: str
    data: dict[str, Any] | Any

    def __init__(self, data: dict[str, Any] | Any, name: str = ""):
        self.data = data
        self.is_dict = isinstance(data, dict)
        self.name = name

    def search(self, path: str) -> Union["ConfigNode", None]:
        """Search for a key in the data"""
        if path == "":
            return self
        if not self.is_dict:
            return None

        keys = path.split(".", maxsplit=1)
        key = keys[0]
        rest = keys[1] if len(keys) > 1 else ""

        match key:
            case "*":
                for k in self.data:  # find first match
                    if node := self.get(k).search(rest):
                        return node
            case _:
                if node := self.get(key):
                    return node.search(rest)
        return None

    def get(self, key: str) -> Union["ConfigNode", Any]:
        if not self.is_dict:
            return None
        if result := self.data.get(key):
            return ConfigNode(result, key)
        return None

    def __getitem__(self, key: str) -> Union["ConfigNode", Any]:
        query = self.search(key)
        if query is None:
            raise KeyError(f"Key {key} not found")
        return query


class ConfigLoader:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.load()

    def __load__(self, config_name: str) -> Any | dict[str, Any] | None:
        predicted_files = [
            Path(CONFIG_PATH / f"{config_name}.yml"),
            Path(CONFIG_PATH / f"{config_name}.yaml"),
        ]

        for file in predicted_files:
            if file.exists():
                return yaml.safe_load(open(str(file), "r"))
        return None

    def load(self) -> dict[str, Any] | None:
        base_config = self.__load__(self.config_file)
        env_config = self.__load__(f"{self.config_file}.{ENVIROMENT}")
        secret_config = self.__load__(f"{self.config_file}.secret")
        local_config = self.__load__(f"{self.config_file}.local")

        if not base_config:
            raise FileNotFoundError(
                f"No base config found at {CONFIG_PATH / self.config_file}.yml"
            )

        config = self.merge_dicts(
            base_config, env_config or {}, secret_config or {}, local_config or {}
        )

        self.root = ConfigNode(config, "root")

    @classmethod
    def merge_dicts(cls, *dicts: dict[str, Any]) -> dict[str, Any]:
        result = {}
        for dictionary in dicts:
            for key, value in dictionary.items():
                if (
                    key in result
                    and isinstance(value, dict)
                    and isinstance(result[key], dict)
                ):
                    result[key] = cls.merge_dicts(result[key], value)
                else:
                    result[key] = value
        return result

    def Field(self, path: str | None = None, env: str | None = None) -> Any | None:
        if path is not None:
            if node := self.root.search(path):
                return node.data
        if env is not None:
            return os.environ.get(env)
        return None

    def __getitem__(self, key: str) -> Any:
        return self.root[key]