import json
from pathlib import Path


class Reader:

    @staticmethod
    def read_saved_files(trello_object: str, board_name: str = None, dir_path: str = None) -> None:

        trello_object = trello_object.lower()

        if trello_object in ("card", "board", "comment", "checklist", "comment", "attachment"):
            if board_name is not None:
                p = Path(f"Data/{board_name}")
            elif dir_path is not None:
                p = Path(f"{dir_path}")
            else:
                print("You need to specify either board_name or dir_path!")
                return

            if p.is_dir():
                print(f"{board_name} - {trello_object.upper()}\n-----------------------------------------")

                for i in p.glob("**/*"):
                    if i.is_file() and i.name.startswith(trello_object):
                        print(i.name)
                        if trello_object != "attachment":
                            Reader.__read_file(i)
            else:
                print("Not Valid Board Name")
        else:
            print("You Didnt Pass A Valid Trello Object")

    @staticmethod
    def __read_file(filename: str) -> None:
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                print(json.dumps(data, indent=4))
        except FileNotFoundError:
            print("There Is No Data About That File In Your System")
