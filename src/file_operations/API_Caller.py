from src.common.trello_client.trello_client import TrelloClient
from src.file_operations.reader import Reader
from src.Models.board import Board
from src.Models.card import Card
from src.Models.checklist import CheckList
from src.Models.comment import Comment
from src.Models.trelloList import TrelloList


def get_everything(board_id: str, client: TrelloClient):
    board = Board.get_board(board_id=board_id, client=client, dir_path="./Data/")
    if board is not None:
        lists = TrelloList.get_lists(board_id=board_id, client=client, dir_path=board.get_directory())
        for trello_list in lists:
            cards = Card.get_cards(list_id=trello_list.id, client=client, dir_path=trello_list.get_directory())
            if cards:
                for card in cards:
                    if card.badges.get("comments") != 0:
                        Comment.get_comments(client=client, card_id=card.id, dir_path=card.get_directory())
                        CheckList.get_checklists(client=client, card_id=card.id, dir_path=card.get_directory())


def save_cards_to_trello(board_name: str, client: TrelloClient):
    cards = Reader.read_saved_files(trello_object=Card, board_name=board_name)
    if cards is not None and cards != []:
        for card in cards:

            card_response = client.post(
                endpoint="/cards",
                params={
                    "name": card.name,
                    "desc": card.desc,
                    "pos": card.pos,
                    "due": card.due,
                    "start": card.start,
                    "dueComplete": card.dueComplete,
                    "idList": card.idList,
                    "idMembers": card.idMembers,
                    "idLabels": card.idLabels,
                },
            )

            comments = Reader.read_saved_files(trello_object=Comment, dir_path=card.get_directory())

            if comments is not None and comments != []:
                for comment in comments:
                    client.post(
                        endpoint=f"/cards/{card_response.get('id')}/actions/comments",
                        params={"text": comment.text},
                    )

            checklist_list = Reader.read_saved_files(trello_object=CheckList, dir_path=card.get_directory())

            if checklist_list is not None and checklist_list != []:
                for checklist in checklist_list:

                    checklist_response = client.post(
                        endpoint=f"/cards/{card_response.get('id')}/checklists", params={"name": checklist.name}
                    )

                    if checklist.checkItems is not None and checklist.checkItems != []:
                        for checkItem in checklist.checkItems:

                            client.post(
                                endpoint=f"/checklists/{checklist_response.get('id')}/checkItems",
                                params={
                                    "name": checkItem.name,
                                    "checked": "false" if checkItem.state == "incomplete" else "true",
                                },
                            )
        print(f"All Cards From: {board_name} Added To Trello Board!")
    else:
        print("There Are No Cards In That Board!")
