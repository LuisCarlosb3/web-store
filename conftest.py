import pytest
from rest_framework.authtoken.models import Token


@pytest.fixture
def store_client(client):
    class RequestClient:
        def __init__(self) -> None:
            self.client = client

        def __make_token_header(self, token):
            return {
                'CONTENT_TYPE': "application/json",
                'HTTP_AUTHORIZATION': f'Token {token}'
            }

        def make_user_token(self, user):
            token, _ = Token.objects.get_or_create(user=user)
            return token.key

        def login(self, payload):
            return self.client.post("/api/users/login/", payload)

        def register(self, payload):
            return self.client.post("/api/users/", data=payload, content_type="application/json")

        def list_users(self, token=''):
            headers = self.__make_token_header(token)
            return self.client.get("/api/users/", **headers)

        def retrieve_user(self, user_id, token=''):
            headers = self.__make_token_header(token)
            return self.client.get(f"/api/users/{user_id}/", **headers)

    return RequestClient()
