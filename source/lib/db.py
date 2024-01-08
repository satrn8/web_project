from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker



class DB():
    def __init__(self, connect_data: str) -> None:
        self.connect_data = connect_data
        self.db_session = None
        self.engine = None
        self.Base = None

    def connect(self) -> None:
        # подключение к базе данных
        self.engine = create_engine(self.connect_data)
        # проверка подключения
        connection = self.engine.connect()
        if connection.ping():
            print("Подключение успешно установлено!")
        else:
            print("Не удалось подключиться к базе данных")
        
    def session(self) -> None:
        # Создание сессии
        if self.engine:
            self.db_session = scoped_session(sessionmaker(bind=self.engine))
            self.Base = declarative_base()
            self.Base.query = self.db_session.query_property()
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
