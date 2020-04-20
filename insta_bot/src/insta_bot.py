import requests
from .endpoints import endpoints

class instaBot:
    def __init__(self):
        self.session = requests.Session()
        r = self.session.get('https://www.instagram.com/')


session = requests.Session()
csrf_token = session.cookies['csrftoken']
session.headers.update({'X-CSRFToken': csrf_token})
response = session.post('https://www.instagram.com/accounts/login/ajax/', data={'username': '_hellboybjj', 'password': 'R@f@elrrx123'})
