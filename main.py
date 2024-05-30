from src.common.trello_client.trello_client import TrelloClient
from src.file_operations.API_Caller import get_everything
from src.file_operations.reader import Reader
from src.Models.board import Board
from src.Models.card import Card
from src.Models.checklist import CheckItem, CheckList
from src.Models.comment import Comment
from src.Models.trelloList import TrelloList
from src.orm.db_connection import DB_Connection


def create_object(trello_obj):
    data = Reader.read_saved_files(trello_object=trello_obj, board_name="Zadaci Za Automatizaciju", print_result=False)
    DB_Connection.add_object(data)


if __name__ == "__main__":

    # Kupljenje Date Sa Trello Boarda
    # client = TrelloClient()  # Radi
    # get_everything(board_id="SqLhSk0r", client=client)

    # Pravaljenje Tabela U Bazi
    # DB_Connection.create_tables()

    # CRUD

    # Create
    # Board
    # create_object(Board)

    # Trello List
    # create_object(TrelloList)

    # Card
    # create_object(Card)

    # CheckList
    # create_object(CheckList)

    # Comment
    # create_object(Comment)

    # Read All
    # data = DB_Connection.get_object(trello_object=Card)
    # print(data)

    # Update
    # data = DB_Connection.get_object(trello_object=Card)
    # print(data[1].name)
    # data[0].name = "Nauciti SQLAlchemy"
    # DB_Connection.update_object(data[0])

    # Delete
    # DB_Connection.delete_object(trello_object=CheckItem, id="6653b2a2079491a72c388d65")

    pass
