import requests

class TrelloClient:

    # API i Token
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1/"

    # Get metoda
    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['key'] = self.api_key
        params['token'] = self.token
        response = requests.get(self.base_url + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    # Post metoda
    def _post(self, endpoint, data=None):
        if data is None:
            data = {}
        data['key'] = self.api_key
        data['token'] = self.token
        response = requests.post(self.base_url + endpoint, json=data)
        response.raise_for_status()
        return response.json()

    # Get board uz pomoc geta
    def get_boards(self):
        return self._get('members/me/boards')

    # Get list uz pomoc geta
    def get_lists(self, board_id):
        return self._get(f'boards/{board_id}/lists')

    # Get kartice uz pomoc geta
    def get_cards(self, list_id):
        return self._get(f'lists/{list_id}/cards')

    # Get checklistu uz pomoc geta
    def get_checklists(self, card_id):
        return self._get(f'cards/{card_id}/checklists')

    # Get komentare uz pomoc geta
    def get_comments(self, card_id):
        return self._get(f'cards/{card_id}/actions', params={'filter': 'commentCard'})

    # Dodavanje kartice uz pomoc posta
    def add_card(self, list_id, name, desc=''):
        data = {
            'idList': list_id,
            'name': name,
            'desc': desc
        }
        return self._post('cards', data)