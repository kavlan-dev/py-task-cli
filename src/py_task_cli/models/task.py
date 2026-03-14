from dataclasses import dataclass


@dataclass
class Task:
    id: int
    description: str
    status: str
    created_at: str
    updated_at: str
