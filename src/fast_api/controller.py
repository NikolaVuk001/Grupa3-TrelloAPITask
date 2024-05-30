import json
import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from src.common.trello_client.trello_client import TrelloClient
from src.fast_api.pydantic_models.models import CardModel, TrelloListModel
from src.models.board import Board
from src.models.card import Card
from src.models.comment import Comment
from src.models.trelloList import TrelloList
from src.orm.db_connection import DB_Connection

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Friend"}


@app.get("/boards/{board_id}")
async def get_board(board_id: str):
    board: Board = DB_Connection.get_object_by_id(trello_object=Board, id=board_id)
    if board is not None:
        result = board.to_dict()

        lists = DB_Connection.get_object_by_attr(
            trello_object=TrelloList, attr_name="idBoard", attr_value=board.id, columns=["id", "name"]
        )
        result["lists"] = [{"id": lst.id, "name": lst.name} for lst in lists] if lists else []

        cards = DB_Connection.get_object_by_attr(
            trello_object=Card, attr_name="idBoard", attr_value=board.id, columns=["id", "name", "url"]
        )

        result["cards"] = [{"id": card.id, "name": card.name, "url": card.url} for card in cards] if cards else []

        return result

    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Message": "No Board Found With That ID"})


@app.get("/cards/{card_id}")
async def get_card(card_id: str):
    card: Card = DB_Connection.get_object_by_id(trello_object=Card, id=card_id)
    if card is not None:
        result = card.to_dict()
        comments = DB_Connection.get_object_by_attr(trello_object=Comment, attr_name="card_id", attr_value=card.id)

        result["comments"] = [{"id": comment.id, "text": comment.text} for comment in comments] if comments else []
        return result
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Message": "No Card Found With That ID"})


@app.get("/lists/{list_id}")
async def get_list(list_id: str):
    trello_list = DB_Connection.get_object_by_id(trello_object=TrelloList, id=list_id)
    if trello_list is not None:
        result = trello_list.to_dict()
        return result
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"Message": "No Trello List Found With That ID"}
        )


@app.post("/card")
def add_card(card: CardModel):
    if card is not None:

        client = TrelloClient()

        post_response = client.post(
            endpoint="/cards", params={"name": card.name, "idList": card.idList, "desc": card.desc, "pos": card.pos}
        )

        if post_response:

            get_response = client.get(endpoint=f"/cards/{post_response.get('id')}")

            new_card: Card = Card.from_json(json.dumps(get_response))

            if DB_Connection.add_object(trello_object=new_card):
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_response)
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Message": "Error With Trello API"}
            )

    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"Message": "You Didnt Pass A Valid Card Object"}
        )


@app.post("/list")
async def add_list(list: TrelloListModel):
    if list is not None:
        client = TrelloClient()

        post_response = client.post(
            endpoint="/lists", params={"name": list.name, "idBoard": list.idBoard, "pos": list.pos}
        )

        if post_response:

            get_response = client.get(endpoint=f"/lists/{post_response.get('id')}")

            new_trello_list = TrelloList.from_json(json.dumps(get_response))

            if DB_Connection.add_object(trello_object=new_trello_list):
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_response)

        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Message": "Error With Trello API"}
            )

    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"Message": "You Didnt Pass A Valid Trello List Object"}
        )
