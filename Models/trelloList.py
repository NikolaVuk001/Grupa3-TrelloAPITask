import json
from dataclasses import dataclass
from os import path
from typing import List

from dataclasses_json import dataclass_json
from Mod.check_dir_existence import ensure_directory_exists
from Mod.trelloClient import TrelloClient


@dataclass_json
@dataclass
class TrelloList:
    id: str
    name: str
    closed: bool
    pos: int
    idBoard: str
    subscribed: bool
    softLimit: str | None

    _directory = path.join(path.dirname(__file__), "../Data/Lists/")

    # Getter za direktorijum

    def get_directory(self) -> str:
        return self._directory

    @staticmethod
    def get_lists(board_id: str, client: TrelloClient, dir_path: str = _directory):

        # Get Zahtev Ka Trellu Pomocu TrelloClient-a
        result = client.get(f"/boards/{board_id}/lists")

        if result is not None:

            lists: List[TrelloList] = []

            # Instanciranje Listi U Klasu
            for list_result in result:
                lists.append(TrelloList.from_json(json.dumps(list_result)))

            # Upisivanje Listi Na Disk Pojedinacno U Zaseban Fajl
            for trello_list in lists:
                if dir_path != TrelloList._directory:
                    trello_list._directory = dir_path + f"Lists/{trello_list.name}/"
                ensure_directory_exists(trello_list._directory)

                with open(trello_list._directory + f"list-{trello_list.id}.json", "w") as f:
                    f.write(trello_list.to_json(sort_keys=True, indent=4, separators=(",", ": ")))

            return lists
