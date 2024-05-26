import json
from dataclasses import dataclass
from os import path

from dataclasses_json import dataclass_json
from Mod.check_dir_existence import ensure_directory_exists
from Mod.trello_client import TrelloClient


@dataclass_json
@dataclass
class Board:
    id: str
    name: str | None
    desc: str | None
    descData: str | None
    url: str | None

    _directory = path.join(path.dirname(__file__), "../Data/Board/")

    # Getter za direktorijum
    def get_directory(self) -> str:
        return self._directory

    def set_directory(self, directory: str) -> None:
        if directory is not None and path.isdir(directory):
            self._directory = directory
        else:
            print("Not A Valid Directory")

    @staticmethod
    def get_board(board_id: str, client: TrelloClient, dir_path: str = _directory):

        # Get Zahtev Ka Trellu Pomocu TrelloClient-a
        result = client.get(f"/boards/{board_id}")

        if result is not None:
            # Instanciranje Board Objekta
            board = Board.from_json(json.dumps(result))

            if dir_path != Board._directory:
                dir_path += f"{board.name}/"
            # Proverava da li dirketorijum postoji,ako ne,pravi ga
            ensure_directory_exists(dir_path)

            board._directory = dir_path

            # Upisivanje Board-a na disk
            with open(dir_path + f"board-{board.id}.json", "w") as f:
                f.write(board.to_json(sort_keys=True, indent=4, separators=(",", ": ")))

            return board
