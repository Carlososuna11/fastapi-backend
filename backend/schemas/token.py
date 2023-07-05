from pydantic import BaseModel
import datetime


class TokenSchema(BaseModel):
    token: str
    issued_at: datetime.datetime = datetime.datetime.now()
