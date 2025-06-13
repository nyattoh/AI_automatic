from pydantic import BaseModel

class Msg(BaseModel):
    sender: str
    receiver: str
    content: str
    tokens: int = 0
