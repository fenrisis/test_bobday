from pydantic import BaseModel


class PostResponse(BaseModel):
    status_code: int
    data_saved: str
