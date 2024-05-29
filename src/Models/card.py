import json
from dataclasses import dataclass
from os import path
from typing import List

from dataclasses_json import dataclass_json
from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry
from src.common.trello_client.trello_client import TrelloClient
from src.Mod.check_dir_existence import ensure_directory_exists
from src.orm.orm_mapper import mapper_registry


@dataclass_json
@dataclass
class Trello:
    board: int | None
    card: int | None


@dataclass_json
@dataclass
class AttachmentsByType:
    trello: Trello | None


@dataclass_json
@dataclass
class Badges:
    attachmentsByType: AttachmentsByType | None
    comments: int | None


@dataclass_json
@dataclass
class Cover:
    idAttachment: str | None
    color: str | None
    idUploadedBackground: bool | None
    size: str | None
    brightness: str | None
    idPlugin: str | None


@mapper_registry.mapped
@dataclass_json
@dataclass
class Card:

    __table__ = Table(
        "card",
        mapper_registry.metadata,
        Column("id", String, primary_key=True),
        Column("badges", JSON),
        # Column("checkItemStates", String),
        Column("closed", Boolean),
        Column("dueComplete", Boolean),
        Column("dateLastActivity", String),
        Column("desc", String),
        Column("due", String),
        Column("dueReminder", String),
        Column("email", String),
        Column("idBoard", String, ForeignKey("board.id")),
        Column("idList", String, ForeignKey("trelloList.id")),
        # Column("idMembers", String),
        # Column("idMembersVoted", String),
        Column("idShort", Integer),
        Column("idAttachmentCover", String),
        # Column("labels", String),
        # Column("idLabels", String),
        Column("manualCoverAttachment", Boolean),
        Column("name", String),
        Column("pos", Integer),
        Column("shortLink", String),
        Column("shortUrl", String),
        Column("start", String),
        Column("subscribed", Boolean),
        Column("url", String),
        Column("cover", JSON),  # JSON
        Column("isTemplate", Boolean),
        Column("cardRole", String),
    )
    id: str | None
    badges: dict | None  # Promenjeno Sa Badges kalse
    # checkItemStates: List[str] | None  # Problem Kako Upisati List[str] u bazu
    closed: bool | None
    dueComplete: bool | None
    dateLastActivity: str | None
    desc: str | None
    due: str | None
    dueReminder: str | None
    email: str | None
    idBoard: str | None
    # idChecklists: List[str] | None Dodati List[CheckList] kao listu svih checklisti unutar Carda
    idList: str | None  # Referenca Na List
    # idMembers: List[str] | None
    # idMembersVoted: List[str] | None
    idShort: int | None
    idAttachmentCover: str | None
    # labels: List[str] | None
    # idLabels: List[str] | None
    manualCoverAttachment: bool | None
    name: str | None
    pos: int | None
    shortLink: str | None
    shortUrl: str | None
    start: str | None
    subscribed: bool | None
    url: str | None
    cover: dict | None
    isTemplate: bool | None
    cardRole: str | None

    _directory = path.join(path.dirname(__file__), "../Data/Cards/")

    # Getter za direktorijum
    def get_directory(self) -> str:
        return self._directory

    def set_directory(self, directory: str) -> None:
        if directory is not None and path.isdir(directory):
            self._directory = directory
        else:
            print("Not A Valid Directory")

    @staticmethod
    def get_cards(list_id: str, client: TrelloClient, dir_path: str = _directory):

        # Get Zahtev Ka Trellu Pomocu TrelloClient-a
        result = client.get(f"/lists/{list_id}/cards")

        if result is not None:

            cards: List[Card] = []

            # Instanciranje Kartica U Klasu
            for card_result in result:
                cards.append(Card.from_json(json.dumps(card_result)))

                # Cuvanje Card Attachment Funkcija
                if card_result.get("cover").get("idAttachment") is not None:
                    Card.__save_attachment(
                        card_id=card_result.get("id"),
                        attachment_id=card_result.get("cover").get("idAttachment"),
                        client=client,
                        dir_path=(
                            dir_path + f"Cards/{card_result.get('name')}" if dir_path != Card._directory else dir_path
                        ),
                    )

            # Upisivanje Kartica Na Disk Pojedinacno U Zaseban Fajl
            for card in cards:
                if dir_path != Card._directory:
                    card._directory = dir_path + f"Cards/{card.name}/"
                ensure_directory_exists(card._directory)
                with open(card._directory + f"card-{card.id}.json", "w") as f:
                    f.write(card.to_json(sort_keys=True, indent=4, separators=(",", ": ")))

            return cards

    # Privatna metoda za cuvanje attachmenta sa kartica u json formatu
    @staticmethod
    def __save_attachment(card_id: str, attachment_id: str, client: TrelloClient, dir_path: str):

        attachment_dir = dir_path + "/Attachments"

        ensure_directory_exists(attachment_dir)

        attachment_result = client.get(f"/cards/{card_id}/attachments/{attachment_id}")
        with open(attachment_dir + f"/attachment-{attachment_id}.json", "w") as f:
            f.write(json.dumps(attachment_result, sort_keys=True, indent=4, separators=(",", ": ")))
