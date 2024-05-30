import copy
import sqlite3
from typing import List, Union

import sqlalchemy.exc
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session, registry
from src.models.board import Board
from src.models.card import Card
from src.models.checklist import CheckList
from src.models.comment import Comment
from src.models.trelloList import TrelloList
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
            except Exception as e:
                print(e)
            else:
                session.commit()

    @staticmethod
    def get_all_objects(
        trello_object: Union[Card, Board, CheckList, Comment, TrelloList]
    ) -> List[Union[Card, Board, CheckList, Comment, TrelloList]]:
        with Session(DB_Connection._engine) as session:
            try:
                data = session.query(trello_object).all()
                return data
            except Exception as e:  # Koj Error Bi Ovde Trebao?
                print(e)

    @staticmethod
    def get_object_by_id(trello_object: Union[Card, Board, CheckList, Comment, TrelloList], id: str):
        with Session(DB_Connection._engine) as session:
            try:
                data = session.query(trello_object).filter_by(id=id).one_or_none()
                return data
            except Exception as e:
                print(e)

    @staticmethod
    def get_object_by_attr(
        trello_object: Union[Card, Board, CheckList, Comment, TrelloList],
        attr_name: str,
        attr_value: str,
        columns: List[str] = None,
    ):
        with Session(DB_Connection._engine) as session:
            try:
                filter_condition = {attr_name: attr_value}
                if columns:
                    column_names = [getattr(trello_object, column) for column in columns]
                    data = session.query(trello_object).with_entities(*column_names).filter_by(**filter_condition).all()
                else:
                    data = session.query(trello_object).filter_by(**filter_condition).all()
                return data
            except Exception as e:
                print(e)

    @staticmethod
    def update_object(trello_object: Union[Card, Board, CheckList, Comment, TrelloList]):  # Ne Radi

        with Session(DB_Connection._engine) as session:
            data = session.query(type(trello_object)).filter_by(id=trello_object.id).one_or_none()
            if data is not None:
                for key, value in trello_object.to_dict().items():
                    setattr(data, key, value)
                try:
                    session.commit()
                except Exception as e:
                    print(e)
            else:
                print("Cant Find Trello Object In DataBase")

    @staticmethod
    def delete_object(trello_object: Union[Card, Board, CheckList, Comment, TrelloList], id: str):
        with Session(DB_Connection._engine) as session:
            result = session.query(trello_object).filter_by(id=id).one_or_none()
            if result is not None:
                try:
                    session.delete(result)
                    session.commit()
                except Exception as e:  # Koj Error Bi Ovde Trebao?
                    print(e)
            else:
                print(f"No {trello_object} with id: {id} in database")

    @staticmethod
    def create_tables():
        mapper_registry.metadata.create_all(DB_Connection._engine)
