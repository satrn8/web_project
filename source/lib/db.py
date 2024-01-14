from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ...config import SQLALCHEMY_DATABASE_URI

from sqlalchemy.exc import OperationalError, NoSuchModuleError

from models import User


class DBError(Exception):
    """Ошибка работы с БД"""


class DB:
    def __init__(self, URL: str) -> None:
        self.URL = URL
        self.session = None
        self.engine = None
        self.base = None
        self.connection = None

    def connect(self) -> object:
        try:
            self.engine = create_engine(self.URL)
            self.engine.connect()
            self.create_session()

        except OperationalError:
            raise DBError('Ошибка в логине, пароле, адресе сервера или самой БД')
        except NoSuchModuleError:
            raise DBError('Не правильно задан модуль БД')

    def create_session(self) -> None:
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def close(self) -> None:
        # Закрытие сессии
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()

    def __repr__(self) -> str:
        return '<DB {}>'.format(self.connect_data)

    def get_users(self) -> list:
        self.connect()

        return self.session.query(User).first().fist_name

    def add_user(self) -> None:
        self.connect()
        user = User(
            login="kek",
            email="kek",
            fist_name="kek",
            last_name="kek",
            patronymic="kek",
            position="kek",
            role="kek",
        )
        self.session.add(user)
        self.session.commit()


db = DB(SQLALCHEMY_DATABASE_URI)

print(db.add_user())