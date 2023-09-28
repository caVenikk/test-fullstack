from src.database import create_database_async_session
from src.repository.products_repository import ProductRepository
from src.repository.users_repository import UserRepository
from src.utils import Singleton


class CRUD(metaclass=Singleton):
    def __init__(self):
        session = create_database_async_session()
        self.users = UserRepository(session)
        self.products = ProductRepository(session)

    def __call__(self):
        return self
