from groupy import Client

class PyGroupMe:
    def __init__(self, token):
        self.token = token
        self.client = Client.from_token(token)
