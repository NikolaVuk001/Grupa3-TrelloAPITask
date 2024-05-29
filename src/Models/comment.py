import json
from dataclasses import dataclass
from os import path
from typing import List

from dataclasses_json import dataclass_json
from sqlalchemy import Column, ForeignKey, String, Table
from src.common.trello_client.trello_client import TrelloClient
from src.Mod.check_dir_existence import ensure_directory_exists
from src.orm.orm_mapper import mapper_registry


@mapper_registry.mapped
@dataclass_json
@dataclass
class Comment:
    __table__ = Table(
        "comment",
        mapper_registry.metadata,
        Column("id", String, primary_key=True),
        Column("text", String),
        Column("card_id", String, ForeignKey("card.id")),
    )

    id: str
    text: str | None
    card_id: str | None

    _directory = path.join(path.dirname(__file__), "../../Data/")

    def __init__(self, id: str, text: str, card_id: str):
        self.id = id
        self.text = text
        self.card_id = card_id

    # Getter za direktorijum
    @staticmethod
    def get_directory() -> str:
        return Comment._directory

    def set_directory(self, directory: str) -> None:
        if directory is not None and path.isdir(directory):
            self._directory = directory
        else:
            print("Not A Valid Directory")

    # Get komentare uz pomoc geta
    @staticmethod
    def get_comments(client: TrelloClient, card_id: str, dir_path: str = _directory):

        # Proverava da li dirketorijum postoji,ako ne,pravi ga

        result = client.get(f"/cards/{card_id}/actions")

        if result is not None:

            comments: List[Comment] = []

            for comment_dict in result:
                comments.append(
                    Comment(
                        id=comment_dict.get("id"),
                        text=comment_dict.get("data").get("text"),
                        card_id=comment_dict.get("data").get("card").get("id"),
                    )
                )
            for comment in comments:
                comment._directory = dir_path + f"Comments/"
                ensure_directory_exists(comment._directory)
                with open(comment._directory + f"comment-{comment.id}.json", "w") as f:
                    json.dump(comment, f, default=lambda o: o.__dict__, indent=4)

            # return comments <<< Ako je potrebno vratiti listu dobijenih komentara
