from pydantic import BaseModel

class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class TelexMessagePayload(BaseModel):
    content: str