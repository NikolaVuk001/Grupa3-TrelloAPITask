import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RetryError

# API i TOKEN
API = ""
TOKEN = ""

# ID mog borda
BOARD_ID = "d1IUCCHh"

# Lista ID
LIST_ID = "6646043acd85359f0f9bbbaf"


# Funkcija za citanje svih kartca sa board-a
def read_cards(session: requests.Session) -> None:

    response = session.get(f"https://api.trello.com/1/boards/{BOARD_ID}/cards")

    cards = response.json()

    for card in cards:
        print("Ime karte: ", card["name"])
        print("Deskpripcija karte: ", card["desc"])
        print("")


# Funkcija za dodavanje nove kartice u listu
def add_card(session: requests.Session) -> None:
    session.params["idList":str] = LIST_ID
    # Zeljeno ime i deskripciju kartice koje zelimo da unesemo
    session.params["name":str] = input("Unesi ime kartice: ")
    session.params["desc":str] = input("Unesite zeljenu deskripciju karte: ")

    # Slanje POST requesta Trellu za dodavanje nove kartice
    response = session.post("https://api.trello.com/1/cards")

    # Kreiranje i ispisvanje novododate kartice
    new_task = response.json()
    print("Uspesno dodata kartica!")
    print("Id kartice: ", new_task["id"])
    print("Ime kartice: ", new_task["name"])
    print("Deskripcija kartice: ", new_task["desc"])


if __name__ == "__main__":

    # Upit korisnika koju funkcijonalnos zeli
    # TODO Ako je moguce formulistie ovo bolje
    action: str = input("Sta Zelite Da Uradite (Citanje Svih Kartica - 1 | Unos Nove Kartice - 2)\n")

    # Ponovni unos dok ne unese dobar input
    while action != "1" and action != "2":
        action = input("Sta Zelite Da Uradite (Citanje Svih Kartica - 1 | Unos Nove Kartice - 2)\n")

    # Retry objekat za prevenciju preopterecena prilikom neuspesnog poziva API-a
    retries = Retry(total=6, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)

    # Otvaranje sesije
    with requests.session() as current_session:
        # Postavljanje adaptera u session
        current_session.mount(prefix="https://", adapter=adapter)

        # Postavljanje kredencijala
        current_session.params = {"key": API, "token": TOKEN}

        try:
            if action == "1":
                read_cards(current_session)
            else:
                add_card(current_session)

        except RetryError:
            print("Retry error occurred")
        except Exception:
            print("Unexpected error occurred")
