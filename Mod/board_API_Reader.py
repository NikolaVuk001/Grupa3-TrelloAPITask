from Models.board import Board
from Models.card import Card
from Models.checklist import CheckList
from Models.comment import Comment
from Models.trelloList import TrelloList

from Mod.trelloClient import TrelloClient


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
