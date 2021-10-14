from typing import Iterable, TypedDict

class NewAdress(TypedDict):
    street:str
    number:str
    complement:str
    district:str
    city:str
    state:str

class NewUser(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    address:Iterable[NewAdress]

class NewUserSerializer(NewUser):
    confirm_password: str

class UserLogin(TypedDict):
    email: str
    password: str