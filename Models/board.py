import json
from dataclasses import dataclass
from os import path
from typing import List

from dataclasses_json import dataclass_json
from Mod.check_dir_existence import ensure_directory_exists
from Mod.trello_client import TrelloClient


@dataclass_json
@dataclass
class SwitcherViews:
    viewType: str | None
    enabled: bool | None


@dataclass_json
@dataclass
class Prefs:
    permissionLevel: str | None
    hideVotes: bool | None
    voting: str | None
    comments: str | None
    invitations: str | None
    selfJoin: bool | None
    cardCovers: bool | None
    cardCounts: bool | None
    isTemplate: bool | None
    cardAging: str | None
    calendarFeedEnabled: bool | None
    hiddenPluginBoardButtons: List[str] | None
    switcherViews: List[SwitcherViews] | None
    background: str | None
    backgroundColor: str | None
    backgroundImage: str | None
    backgroundTile: bool | None
    backgroundBrightness: str | None
    sharedSourceUrl: str | None
    backgroundImageScaled: str | None
    backgroundBottomColor: str | None
    backgroundTopColor: str | None
    canBePublic: bool | None
    canBeEnterprise: bool | None
    canBeOrg: bool | None
    canBePrivate: bool | None
    canInvite: bool | None


@dataclass_json
@dataclass
class LabelNames:
    green: str | None
    yellow: str | None
    orange: str | None
    red: str | None
    purple: str | None
    blue: str | None
    sky: str | None
    lime: str | None
    pink: str | None
    black: str | None
    green_dark: str | None
    yellow_dark: str | None
    orange_dark: str | None
    red_dark: str | None
    purple_dark: str | None
    blue_dark: str | None
    sky_dark: str | None
    lime_dark: str | None
    pink_dark: str | None
    black_dark: str | None
    green_light: str | None
    yellow_light: str | None
    orange_light: str | None
    red_light: str | None
    purple_light: str | None
    blue_light: str | None
    sky_light: str | None
    lime_light: str | None
    pink_light: str | None
    black_light: str | None


@dataclass_json
@dataclass
class Board:
    id: str | None
    name: str | None
    desc: str | None
    descData: str | None
    closed: bool | None
    idOrganization: str | None
    idEnterprise: str | None
    pinned: bool | None
    url: str | None
    shortUrl: str | None
    prefs: Prefs | None
    labelNames: LabelNames | None

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
