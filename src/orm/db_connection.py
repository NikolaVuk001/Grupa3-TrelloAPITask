import sqlite3
from typing import List, Union

import sqlalchemy.exc
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session, registry
from src.Models.board import Board
from src.Models.card import Card
from src.Models.checklist import CheckList
from src.Models.comment import Comment
from src.Models.trelloList import TrelloList
from src.orm.orm_mapper import mapper_registry


class DB_Connection:
    _url = URL.create("sqlite", database="database.db")
    _engine = create_engine(_url)

    @staticmethod
    def add_object(
        trello_object: (
            Union[Card, Board, CheckList, Comment, TrelloList]
            | Union[List[Card], List[Board], List[CheckList], List[Comment], List[TrelloList]]
        )
    ):

        with Session(DB_Connection._engine) as session:
            session.begin()
            try:
                if type(trello_object) == type([]):
                    session.add_all(trello_object)
                else:
                    session.add(trello_object)

            except sqlalchemy.exc.SQLAlchemyError as e:  # Hvatanje Errora Kako?
                session.rollback()
                print(e)
            else:
                session.commit()

    @staticmethod
    def create_tables():
        mapper_registry.metadata.create_all(DB_Connection._engine)
