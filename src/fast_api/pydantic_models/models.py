from pydantic import BaseModel, Field


class CardModel(BaseModel):
    name: str
    idList: str
    desc: str = Field(default="")
    pos: int = Field(default=1)


class TrelloListModel(BaseModel):
    name: str
    idBoard: str
    pos: int = Field(default=1)
