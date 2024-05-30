import json
import os
from pathlib import Path
from typing import List, Union

from src.models.board import Board
from src.models.card import Card
from src.models.checklist import CheckList
from src.models.comment import Comment
from src.models.trelloList import TrelloList


class Reader:

    @staticmethod
    def read_saved_files(
        trello_object: Union[Card, Board, CheckList, Comment, TrelloList],
        board_name: str = None,
        dir_path: str = None,
        print_result: bool = False,
    ) -> List[Union[Card, Board, CheckList, Comment, TrelloList]] | None:

        # trello_object = f"{trello_object}".lower()
        object_name: str = trello_object.__name__.lower()

        if trello_object in (Card, Board, CheckList, Comment, TrelloList):

            if board_name is not None:
                p = Path(f"Data/{board_name}")
            elif dir_path is not None:
                p = Path(f"{dir_path}")
            else:
                print("You need to specify either board_name or dir_path!")
                return

            if p.is_dir():
                data: List[trello_object] = []

                for i in p.glob("**/*"):
                    if i.is_file() and i.name.startswith(object_name.lower()):

                        data.append(Reader.__read_file(filename=i, trello_object=trello_object))
                        if print_result:
                            print(i.name)
                            print(data[-1].to_json(indent=4))

                return data
            else:
                print("Not Valid Board Name Or A Path")
        else:
            print("You Didnt Pass A Valid Trello Object")

    @staticmethod
    def __read_file(filename: str, trello_object):
        try:
            with open(filename, "r") as f:
                data = trello_object.from_dict(json.load(f))
                # print(json.dumps(data, indent=4)) Printanje U Konzoli Direktno
                data.set_directory(os.path.dirname(filename) + "\\")
                return data

        except FileNotFoundError:
            print("There Is No Data About That File In Your System")
