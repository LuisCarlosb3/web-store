from accounts.models import User


def payload_user_factory(password="123", password_confirm="123", email="email@email.com"):
    return {
        "address": [
            {
                "street": "rua",
                "number": "000",
                "complement": "",
                "district": "bairro",
                "city": "cidade",
                "state": "estado"
            }
        ],
        "password": password,
        "confirm_password": password_confirm,
        "first_name": "novo",
        "last_name": "usuario",
        "email": email
    }


def create_user(is_admin=True, email="super@admin.com", password="123") -> User:
    user = User(
        first_name="an", last_name="user", email=email, is_staff=is_admin, is_active=True, is_trusty=True
    )
    user.set_password(password)
    user.save()
    return user
