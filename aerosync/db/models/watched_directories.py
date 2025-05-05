from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

headers = [
    "id",
    "cloud_provider",
    "path",
    "syncing",
    "last_sync",
    "created_on",
    "updated_on",
]


class WatchedDirectory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cloud_provider: str
    path: str = Field(unique=True)
    syncing: bool = True
    last_sync: Optional[datetime] = None
    created_on: datetime = Field(default_factory=datetime.now)
    updated_on: datetime = Field(default_factory=datetime.now)
