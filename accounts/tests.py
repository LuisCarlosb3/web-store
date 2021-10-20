import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from accounts.models import User

from accounts.test_utils.factory import create_user, payload_user_factory


@pytest.mark.django_db
class TestAccountsViewSets:
    def test_login_success(self, store_client):
        create_user()
        payload = {'email': "super@admin.com", 'password': "123"}
        response = store_client.login(payload)
        assert response.status_code == HTTP_200_OK
        assert 'token' in response.data

    def test_login_with_wrong_credentials(self, store_client):
        payload = {'email': "super@admin.com", 'password': "321"}
        response = store_client.login(payload)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.data["message"] == "E-mail ou senha não conferem"

    def test_login_with_invalid_payload(self, store_client):
        payload = {'email': "super@admin.com"}
        response = store_client.login(payload)
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_register_with_success(self, store_client):
        payload = payload_user_factory()
        payload.get("address")
        response = store_client.register(payload)
        assert response.status_code == HTTP_201_CREATED

    def test_register_with_existing_email(self, store_client):
        create_user(email="user@email.com")
        payload = payload_user_factory(email="user@email.com")
        response = store_client.register(payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["email"][0] == "user com este email já existe."

    def test_register_with_invalid_payload(self, store_client):
        payload = payload_user_factory()
        payload.pop("address")
        response = store_client.register(payload)
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_list_users_without_credential(self, store_client):
        response = store_client.list_users()
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_list_users_without_admin_privileges(self, store_client):
        user = create_user(is_admin=False)
        token = store_client.make_user_token(user)
        response = store_client.list_users(token=token)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_list_users(self, store_client):
        user = create_user(password="123")
        token = store_client.make_user_token(user)
        response = store_client.list_users(token=token)
        assert response.status_code == HTTP_200_OK

    def test_user_retrieve_self_info(self, store_client):
        user: User = create_user()
        token = store_client.make_user_token(user)
        response = store_client.retrieve_user(user.id, token=token)
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == user.id
        assert response.data['email'] == user.email

    def test_user_retrieve_other_user_info(self, store_client):
        user: User = create_user(is_admin=False)
        other_user = create_user(email="another@user.com")
        token = store_client.make_user_token(user)
        response = store_client.retrieve_user(other_user.id, token=token)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_user_retrieve_other_user_info_on_admin(self, store_client):
        user: User = create_user(is_admin=True)
        other_user = create_user(email="another@user.com")
        token = store_client.make_user_token(user)
        response = store_client.retrieve_user(other_user.id, token=token)
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == other_user.id
        assert response.data['email'] == other_user.email
