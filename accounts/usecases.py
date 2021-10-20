from typing import Union
from accounts.models import User, UserAddress
from accounts.types import NewUser, UserLogin


def create_user_account(user_payload: NewUser) -> User:
    addresses = user_payload.pop("address")
    password = user_payload.pop("password")
    user_account: User = User.objects.create(**user_payload)
    user_account.set_password(password)
    for addr in addresses:
        UserAddress.objects.create(user=user_account, **addr)
    user_account.save()
    return user_account
