from pydantic import BaseModel
from typing import List


class Book(BaseModel):
    title: str
    description: str
    authors: List[str]
    cover: str
