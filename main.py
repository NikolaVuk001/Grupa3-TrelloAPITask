from Mod.board_API_Reader import get_everything
from Mod.readData import Reader
from Mod.trelloClient import TrelloClient
from Models.board import Board
from Models.card import Card
from Models.checklist import CheckList
from Models.comment import Comment
from Models.trelloList import TrelloList

if __name__ == "__main__":

    # Instanciranje Clienta
    client = TrelloClient()

    # Instanciranje i Cuvanje Fajlova sa API-a:

    # Citanje Celog Boarda
    # --------------------------------------------------------------#
    # get_everything(board_id="SqLhSk0r", client=client)

    # Card
    # --------------------------------------------------------------#
    # Card.get_cards(list_id="6643bc7dfd53e55fab54c01b", client=client)

    # Board
    # --------------------------------------------------------------#
    # Board.get_board(board_id="SqLhSk0r", client=client)

    # Liste
    # --------------------------------------------------------------#
    # TrelloList.get_lists(board_id="SqLhSk0r", client=client)

    # Comments
    # --------------------------------------------------------------#
    # Comment.get_comments(client=client, card_id="66446b2db5f3ce241dc6f371")

    # Check Liste
    # --------------------------------------------------------------#
    # CheckList.get_checklists(card_id="6643bc7eacb9bfbb99d9358f", client=client)

    # Citanje fajlova
    # --------------------------------------------------------------#
    # Citanje iz Vec Postojeceg Board-a
    # Reader.read_saved_files(trello_object="card", board_name="Zadaci Za Automatizaciju")

    # Citanje Iz Specificnog fajla
    # Reader.read_saved_files(trello_object="card", dir_path=os.path.join(os.path.dirname(__file__), "Data/Cards/"))

    # Dodati Vracanje kartica Na Trello
