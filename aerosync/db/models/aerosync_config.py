from datetime import datetime
from sqlmodel import Field, SQLModel


class AerosyncConfig(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    folder_id: str = Field(unique=True)
    cloud_provider: str = Field(unique=True)
    created_on: datetime = Field(default_factory=datetime.now)
    updated_on: datetime = Field(default_factory=datetime.now)
