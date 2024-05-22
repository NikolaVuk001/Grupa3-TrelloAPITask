# Import OS radi pravljenja direktorijuma i file pathovima ATTAa4e4a74262a86c123af88940b3f243aba0bc3298bdfa86d77f20c3074b9d6719BF839615

import os
from Zadatak.Retrive_data import retrieve_and_instantiate, save_to_json
from Zadatak.client import TrelloClient
import re

# Proverava da li dirketorijum postoji,ako ne,pravi ga (valjda?)
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    # API key i token
    api_key = '42464e41c5b7ac2ca9e11577399d13bd'
    while True:
        try:
            token = input("--(Izlaz - 0)-- Unesite API Token: ")
            api_token = token.strip()
            if token == '0':
                print("Izlaz...")
                exit(0)
            # Regex validacija unesenog API tokena
            if not re.match("^ATTA[A-Za-z0-9]{72}$", token):
                print("Pogrešan unos.")
            else:
                break
        except KeyboardInterrupt:
            exit(1)
    client = TrelloClient(api_key, token)

    # Uzima podatke od Retrieve_data.py
    boards = retrieve_and_instantiate(client)

    # stavi svoj direktorijum
    directory = 'D:\zezba'
    ensure_directory_exists(directory)

    #Savuj sve bordove  i liste+kartice(Lista i kartica moraju da budu zajedno zbog read-a,moze i sve zajedno da se stavi kao 3 nested for petlje)
    for board in boards:
        save_to_json(board, os.path.join(directory, f'board_{board.id}.json'))
        for lst in board.lists:
            save_to_json(board, os.path.join(directory, f'board_{lst.id}.json'))
            for card in lst.cards:
                # Add 'idList' to card data before saving
                card_data = card.__dict__.copy()
                card_data['idList'] = lst.id
                save_to_json(card_data, os.path.join(directory, f'card_{card.id}.jsonlist_{lst.id}.json'))
                for checklist in card.checklists:
                    save_to_json(checklist, os.path.join(directory, f'checklist_{checklist.id}.json'))
    print("Sve je sacuvano :)")


if __name__ == '__main__':
    main()