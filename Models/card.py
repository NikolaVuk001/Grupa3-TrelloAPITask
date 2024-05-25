import json
from dataclasses import dataclass
from os import path
from typing import List

from dataclasses_json import dataclass_json
from Mod.check_dir_existence import ensure_directory_exists
from Mod.trelloClient import TrelloClient


@dataclass_json
@dataclass
class Card:
    id: str
    name: str
    desc: str
    idList: str
    idChecklists: str | None
    badges: dict

    _directory = path.join(path.dirname(__file__), "../Data/Cards/")

    # Getter za direktorijum
    def get_directory(self) -> str:
        return self._directory

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
