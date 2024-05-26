import json
from dataclasses import dataclass
from os import path
from typing import List

from dataclasses_json import dataclass_json
from Mod.check_dir_existence import ensure_directory_exists
from Mod.trello_client import TrelloClient

from .checkItem import CheckItem


@dataclass_json
@dataclass
class CheckList:
    id: str
    name: str
    checkItems: List[CheckItem]

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
