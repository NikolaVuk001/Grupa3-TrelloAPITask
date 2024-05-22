import json
from Zadatak.models.board import Board, TrelloList, Card, Checklist,Comment
from Zadatak.client import TrelloClient

def extract_relevant_fields(data, model_class):
    """
    Extract only the relevant fields from the data dictionary based on the fields defined in the model class.
    """
    # Ova funkcija uzima rečnik podataka i klasu modela. Iz rečnika izdvaja samo one parove ključ/vrednost koji odgovaraju poljima definisanim u klasi modela.
    fields = {field for field in model_class.__dataclass_fields__}
    return {key: value for key, value in data.items() if key in fields}


# Uzima Trello API,procesuira ga i stavlja u data klase
def retrieve_and_instantiate(client: TrelloClient):
    boards_json = client.get_boards()
    boards = [Board(**extract_relevant_fields(board, Board)) for board in boards_json]

    for board in boards:
        lists_json = client.get_lists(board.id)
        board.lists = [TrelloList(**extract_relevant_fields(lst, TrelloList)) for lst in lists_json]

        for lst in board.lists:
            cards_json = client.get_cards(lst.id)
            lst.cards = [Card(**extract_relevant_fields(card, Card)) for card in cards_json]

            for card in lst.cards:
                checklists_json = client.get_checklists(card.id)
                card.checklists = [Checklist(**extract_relevant_fields(checklist, Checklist)) for checklist in checklists_json]

                comments_json = client.get_comments(card.id)
                card.comments = [Comment(**extract_relevant_fields(comment, Comment)) for comment in comments_json]

    return boards

# Savuje objekat kao JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, default=lambda o: o.__dict__, indent=4)