import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RetryError, HTTPError
import re


# API KEY
API_KEY = "42464e41c5b7ac2ca9e11577399d13bd"
# ID borda
BOARD_ID = 'SqLhSk0r'
# ID liste
LIST_ID = "6643bc7dfd53e55fab54c01b"


# Funkcija za citanje svih kartca sa board-a
def read_cards(session: requests.Session) -> None:

    # Ako je response = session.get u try bloku, postojace warning za response.status_code unutar except-a:
    # Local variable 'response' might be referenced before assignment
    # Isto vazi i za response = session.post u add_card funkciji
    response = session.get(f"https://api.trello.com/1/boards/{BOARD_ID}/cards")
    try:
        response.raise_for_status()  # HTTPError exception za status_code > 400
        cards = response.json()

        print("")
        for card in cards:
            print("---------------------------------------------------")
            print(f"{card['idShort']}. Kartica\nNaslov:", card['name'])
            print("Deskpripcija: ", card["desc"])
            print("URL:", card['shortUrl'])
    except HTTPError:
        print(f"Došlo je do greške sa Trello web serverom: {response.status_code}")


# Funkcija za dodavanje nove kartice u listu
def add_card(session: requests.Session) -> None:
    # session.params["idList":str] = LIST_ID --> zbog :str desiće se sledeći Exception iako su svi parametri tipa str?
    # Unexpected error occurred: TypeError - unhashable type: 'slice'
    # A ako nema :str desi se warning

    session.params["idList"] = LIST_ID

    # Unos naziva nove kartice
    while True:
        try:
            session.params["name"] = input("--(Izlaz - 0)-- Unesite naziv kartice: ")
            if session.params["name"] == '0':
                print("Izlaz...")
                exit(0)
            if not re.match(r"^[-A-Za-z0-9 ():'\",.@]+$", session.params["name"]):
                print("Pogrešan unos naziva kartice.")
            else:
                break
        except KeyboardInterrupt:
            exit(1)

    # Unos deskripcije nove kartice
    while True:
        try:
            session.params["desc"] = input("--(Izlaz - 0)-- Unesite deskripciju kartice: ")
            if session.params["desc"] == '0':
                print("Izlaz...")
                exit(0)
            if not re.match(r"^[-A-Za-z0-9\s,.?\":]{1,1000}$", session.params["desc"]):
                print("Pogrešan unos deskripcije kartice.")
            else:
                break
        except KeyboardInterrupt:
            exit(1)

    # Slanje POST requesta Trellu za dodavanje nove kartice
    response = session.post("https://api.trello.com/1/cards")
    try:

        response.raise_for_status()  # HTTPError exception za status_code > 400

        # Kreiranje i ispis podataka nove kartice
        new_task = response.json()
        print("")
        print("Uspesno dodata kartica!")
        print("---------------------------------------------------")
        print("ID: ", new_task["id"])
        print("Naziv: ", new_task["name"])
        print("Deskripcija: ", new_task["desc"])
        print("URL:", new_task['shortUrl'])
    except HTTPError:
        print(f"Došlo je do greške sa Trello web serverom: {response.status_code}")


if __name__ == "__main__":

    # Upit korisnika koju funkcijonalnost zeli
    while True:
        try:
            action: str = input("Šta želite da uradite? (Ispis svih kartica - 1 | Unos nove kartice - 2 )\n")
            action = action.strip()
            if action != "1" and action != "2":
                print("Pogrešan unos.")
            else:
                break
        except KeyboardInterrupt:
            exit(1)

    # do while petlja dok se ne unese pravilan API token ili 0
    while True:
        try:
            api_token = input("--(Izlaz - 0)-- Unesite API Token: ")
            api_token = api_token.strip()
            if api_token == '0':
                print("Izlaz...")
                exit(0)
            # Regex validacija unesenog API tokena
            if not re.match("^ATTA[A-Za-z0-9]{72}$", api_token):
                print("Pogrešan unos.")
            else:
                break
        except KeyboardInterrupt:
            exit(1)

    # Retry objekat za prevenciju preopterecenja prilikom neuspesnog poziva API-a
    retries = Retry(total=6, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)

    # Otvaranje sesije
    with requests.session() as current_session:
        # Postavljanje adaptera u session
        current_session.mount(prefix="https://", adapter=adapter)

        # Postavljanje kredencijala
        current_session.params = {"key": API_KEY, "token": api_token}

        try:
            if action == "1":
                read_cards(current_session)
            if action == "2":
                add_card(current_session)
        except RetryError:
            print("Retry error occurred.")
        except Exception as e:
            print(f"Unexpected error occurred: {type(e).__name__}")
        finally:
            current_session.close()
