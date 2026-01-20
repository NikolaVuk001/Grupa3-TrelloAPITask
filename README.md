# Trello Data Backup & Restoration Tool

This project uses the Trello API to fetch boards, lists, cards, comments, and checklists,
save them locally as JSON files, optionally persist them into a SQLite database, and expose
the data through a FastAPI service.

## Features
- Fetch board, list, card, comment, and checklist data from Trello.
- Save JSON files under a `Data/` folder structure by board/list/card.
- Create a SQLite database (`database.db`) and store Trello objects via SQLAlchemy.
- FastAPI endpoints for reading from the database and creating cards/lists on Trello.
- Option to push locally saved cards back to Trello.

## Project structure
- `main.py` - commented usage examples (fetch, DB setup, CRUD).
- `src/Config/config.py` - Trello API credentials.
- `src/common/trello_client/` - HTTP client with retry logic.
- `src/file_operations/` - Trello API calls and JSON readers.
- `src/models/` - dataclass models and SQLAlchemy tables.
- `src/orm/` - database connection and CRUD helpers.
- `src/fast_api/` - FastAPI controller and Pydantic models.

## Requirements
- Python 3.10+ (uses `str | None` typing).
- Packages: `requests`, `sqlalchemy`, `dataclasses-json`, `fastapi`, `pydantic`, `uvicorn`.

Example install:
```bash
pip install requests sqlalchemy dataclasses-json fastapi pydantic uvicorn
```

## Configuration
Fill in Trello credentials in `src/Config/config.py`:
- `API_KEY` and `TOKEN` are required for Trello API access.
- `BOARD_ID` and `LIST_ID` are optional helper values for examples.

## Usage

### 1) Fetch Trello data to JSON
```python
from src.common.trello_client.trello_client import TrelloClient
from src.file_operations.API_Caller import get_everything

client = TrelloClient()
get_everything(board_id="YOUR_BOARD_ID", client=client)
```
Files are created under `Data/<Board Name>/` with subfolders for lists, cards, comments, and checklists.

### 2) Create database tables
```python
from src.orm.db_connection import DB_Connection

DB_Connection.create_tables()
```

### 3) Load JSON files into the database
```python
from src.file_operations.reader import Reader
from src.models.card import Card
from src.orm.db_connection import DB_Connection

cards = Reader.read_saved_files(trello_object=Card, board_name="Zadaci Za Automatizaciju")
DB_Connection.add_object(cards)
```
`main.py` already contains additional commented examples for CRUD operations.

### 4) Run the FastAPI service
```bash
uvicorn src.fast_api.controller:app --reload
```

## FastAPI routes
- `GET /boards/{board_id}` - returns a board with lists and cards.
- `GET /lists/{list_id}` - returns a single list.
- `GET /cards/{card_id}` - returns a card with comments.
- `POST /card` - creates a Trello card (body: `name`, `idList`, `desc`, `pos`).
- `POST /list` - creates a Trello list (body: `name`, `idBoard`, `pos`).

## Push local cards to Trello
```python
from src.common.trello_client.trello_client import TrelloClient
from src.file_operations.API_Caller import save_cards_to_trello

client = TrelloClient()
save_cards_to_trello(board_name="Zadaci Za Automatizaciju", client=client)
```

## Notes
- `database.db` is created in the project root.
- GET routes require data to be saved in the database first.
