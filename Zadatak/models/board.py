from dataclasses import dataclass
from typing import List

@dataclass
class Board:
    id: str
    name: str
    desc: str
    lists: List['List'] = None  # Forward reference
@dataclass
class TrelloList:
    id: str
    name: str
    cards: List['Card'] = None

@dataclass
class Card:
    id: str
    name: str
    desc: str
    checklists: List['Checklist'] = None  # Forward reference
    comments: List['Comment'] = None  # Forward reference

@dataclass
class Checklist:
    id: str
    name: str
    items: List[str]

@dataclass
class Comment:
    id: str
    text: str

