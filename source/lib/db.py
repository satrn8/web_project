from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.exc import OperationalError, NoSuchModuleError



class DB:
    def __init__(self, connect_data: str) -> None:
        self.connect_data = connect_data
        self.db_session = None
        self.engine = None
        self.base = None
        self.connection = None

    def connect(self) -> object:
        # подключение к базе данных
        self.engine = create_engine(self.connect_data)
        # проверка подключения
        try:
            connection = self.engine.connect()
            return connection
        except OperationalError:
            print('Ошибка в логине, пароле, адресе сервера или самой БД')
            return None
        except NoSuchModuleError:
            print('Не правильно задан модуль БД')
            return None
        
    def session(self) -> None:
        # Создание сессии
        if self.engine:
            self.db_session = scoped_session(sessionmaker(bind=self.engine))
            self.base = declarative_base()
            self.base.query = self.db_session.query_property()
        else:
            print("DB is not connected")

    def close(self) -> None:
        # Закрытие сессии
        if self.db_session:
            self.db_session.close()
        if self.engine:  
            self.engine.dispose()

    def __repr__(self) -> str:
        return '<DB {}>'.format(self.connect_data)
