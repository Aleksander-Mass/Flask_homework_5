from pydantic import BaseModel
from uuid import uuid4, UUID


class User(BaseModel):
    id_: UUID = uuid4()
    name: str
    email: str
    password: str