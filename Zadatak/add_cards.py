import os
import json
from Zadatak.client import TrelloClient


# Adduje kartice iz json-a,sa pocetkom card_(tu je listID isto) (verovatno moze bolje,nisam siguran trenutno kako)
def add_cards_from_json(client, directory):
    for filename in os.listdir(directory):
        if filename.startswith('card_') and filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                card_data = json.load(file)

                # idList i name su tu
                if 'idList' not in card_data:
                    print(f"Error: 'idList' not found in {filename}")
                    continue

                if 'name' not in card_data:
                    print(f"Error: 'name' not found in {filename}")
                    continue

                # Uzima korisne podatke
                list_id = card_data['idList']
                name = card_data['name']
                desc = card_data.get('desc', '')

                # Adduje karticu na trello
                new_card = client.add_card(list_id, name, desc)

                # Poruka da je uspesno odradjeno
                print(f"Added card {name} with id {new_card['id']} to list {list_id}")


def main():
    api_key = '42464e41c5b7ac2ca9e11577399d13bd'
    token = 'ATTAa4e4a74262a86c123af88940b3f243aba0bc3298bdfa86d77f20c3074b9d6719BF839615'
    client = TrelloClient(api_key, token)

    # stavi svoj direktorijum
    directory = 'D:\zezba' #stavi svoj direktorijum
    add_cards_from_json(client, directory)


if __name__ == '__main__':
    main()