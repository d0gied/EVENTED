from typing import Any, Literal, Self, Union
import yaml
from pathlib import Path
import os
from abc import ABC

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/config"))
if not CONFIG_PATH.exists():
    raise FileNotFoundError(
        f"No configs found at {CONFIG_PATH}, please set the CONFIG_PATH environment variable"
    )
ENVIROMENT = os.environ.get("ENVIROMENT", "development")
if ENVIROMENT not in ["development", "production"]:
    raise ValueError("ENVIROMENT environment variable should be set to 'development' or 'production'")

class Config(ABC):
    config_name: str
    
    # def __init__(self):
    #     if self.__class__ == Config:
    #         super().__init__()
    #     else:
    
    def __new__(cls):
        if cls == Config: # for root class
            return super().__new__(cls)
        return cls.load()
    
    @classmethod
    def get(cls) -> Self:
        return cls.load()

    @classmethod
    def load(cls, config_name: str | None = None) -> Self:
        if config_name is None:
            config_name = cls.config_name
        if not hasattr(cls, "__config__"):  # singleton pattern
            cls.__config__ = {}
        if config_name not in cls.__config__:
            cls.__config__[config_name] = cls.__load__(config_name)
        return cls.__config__[config_name]

    @classmethod
    def __load__(cls, config_name: str) -> Self:
        common_config = cls.__get_config__(config_name)
        secret_config = cls.__get_config__(f"{config_name}.secret")
        local_config = cls.__get_config__(f"{config_name}.local")
        
        if common_config is None:
            raise FileNotFoundError(f"No config found for {config_name}")

        env_config = cls.__get_config__(f"{config_name}.{ENVIROMENT}")

        result_config = cls.deep_merge_dicts(
            *[
                common_config,
                env_config or {},
                secret_config or {},
                local_config or {},
            ]
        )
        return cls.from_dict(result_config)

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> Self:
        instance = Config()
        for key, value in config.items():
            if isinstance(value, dict):
                setattr(instance, key, cls.from_dict(value))
            else:
                setattr(instance, key, value)
        return instance  # type: ignore

    @staticmethod
    def deep_merge_dicts(*dicts: dict[str, Any]) -> dict:
        result = {}
        for d in dicts:
            for k, v in d.items():
                if isinstance(v, dict):
                    result[k] = Config.deep_merge_dicts(result.get(k, {}), v)
                else:
                    result[k] = v
        return result

    @staticmethod
    def __get_config__(config_name: str) -> dict[str, Any] | None:
        """loads config dict by name from /config, returns None if not found"""

        predicted_paths = [
            CONFIG_PATH / f"{config_name}.yaml",
            CONFIG_PATH / f"{config_name}.yml",
        ]
        for path in predicted_paths:
            if path.exists():
                with open(path, "r") as file:
                    return yaml.safe_load(file)
        return None
        
    def __tree__(self, level: int = 0) -> str:
        result = ""
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
                result += f"{'  ' * level}{key}:\n{value.__tree__(level + 1)}"
            else:
                result += f"{'  ' * level}{key}: {value}\n"
        return result
    
    @property
    def tree(self, level: int = 0) -> str:
        return self.__tree__()

    def __repr__(self) -> str:
        return self.tree

    class Config:
        extra = "allow"
