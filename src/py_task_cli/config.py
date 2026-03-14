import os
from dataclasses import dataclass


@dataclass
class Config:
    tasks_file: str


def load_config() -> Config:
    return Config(
        tasks_file=get_env_or_default("TASK_FILE", "tasks.json"),
    )


def get_env_or_default(varName: str, defaultVal: str) -> str:
    val = os.getenv(varName)
    if val is None:
        val = defaultVal

    return val
