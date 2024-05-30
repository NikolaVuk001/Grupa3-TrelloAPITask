import json
from dataclasses import dataclass, field
from os import path
from typing import List

from dataclasses_json import dataclass_json
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from src.common.trello_client.trello_client import TrelloClient
from src.file_operations.check_dir_existence import ensure_directory_exists
from src.orm.orm_mapper import mapper_registry


@mapper_registry.mapped
@dataclass_json
@dataclass
class CheckItem:
    __table__ = Table(
        "checkItem",
        mapper_registry.metadata,
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("pos", Integer),
        Column("state", String),
        Column("due", String),
        Column("dueReminder", String),
        Column("idMember", String),
        Column("idChecklist", String, ForeignKey("checkList.id")),
    )
    id: str | None
    name: str | None
    pos: int | None
    state: str | None
    due: str | None
    dueReminder: str | None
    idMember: str | None
    idChecklist: str | None


@mapper_registry.mapped
@dataclass_json
@dataclass
class CheckList:
    __table__ = Table(
        "checkList",
        mapper_registry.metadata,
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("idBoard", String, ForeignKey("board.id")),
        Column("idCard", String, ForeignKey("card.id")),
        Column("pos", Integer),
        Column("dueReminder", String),
        Column("idMember", String),
        Column("idChecklist", String, ForeignKey("checkList.id")),
    )
    id: str | None
    name: str | None
    idBoard: str | None
    idCard: str | None
    pos: int | None
    checkItems: List[CheckItem] | None = field(default_factory=list)

    __mapper_args__ = {
        "properties": {
            "checkItems": relationship("CheckItem"),
        }
    }

    _directory = path.join(path.dirname(__file__), "../Data/CheckLists/")

    # Getter za direktorijum
    def get_directory(self) -> str:
        return self._directory

    def set_directory(self, directory: str) -> None:
        if directory is not None and path.isdir(directory):
            self._directory = directory
        else:
            print("Not A Valid Directory")

    @staticmethod
    def get_checklists(card_id: str, client: TrelloClient, dir_path: str = _directory):
        # Get Zahtev Ka Trellu Pomocu TrelloClient-a

        result = client.get(f"/cards/{card_id}/checklists")

        if result is not None:

            check_lists: List[CheckList] = []

            # Instanciranje CheckListi i Klasu
            for checklist_result in result:
                check_lists.append(CheckList.from_json(json.dumps(checklist_result)))

            # Cuvanje CheckList Objekta Na Disk
            for checklist in check_lists:

                if dir_path != CheckList._directory:
                    checklist._directory = dir_path + f"CheckLists/{checklist.name}/"
                ensure_directory_exists(checklist._directory)

                with open(checklist._directory + f"checklist-{checklist.id}.json", "w") as f:
                    f.write(checklist.to_json(sort_keys=True, indent=4, separators=(",", ": ")))

                return check_lists
