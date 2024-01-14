from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import SQLALCHEMY_DATABASE_URI

from sqlalchemy.exc import OperationalError, NoSuchModuleError

from models import User, Board, Task, Comment, Access


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

    # Функция для добавления пользователя
    def add_user(self, login, email, fist_name, last_name, patronymic, position, role) -> None:
        self.connect()
        user = User(
            login=login,
            email=email,
            fist_name=fist_name,
            last_name=last_name,
            patronymic=patronymic,
            position=position,
            role=role,
        )
        self.session.add(user)
        self.session.commit()

    # Функция для запроса всех пользователей
    def get_users(self) -> list:
        self.connect()
        return self.session.query(User).all()

    # Функция для добавления доски
    def add_board(self, title, owner) -> None:
        self.connect()
        board = Board(
            title=title,
            owner=owner
        )
        self.session.add(board)
        self.session.commit()

    # Функция для запроса всех досок
    def get_board(self) -> list:
        self.connect()
        return self.session.query(Board).all()

    # Функция для добавления задачи
    def add_task(self, board_id, title, description, author, assigned_to, 
                 published, finish_date, planned_finish_date, planned_spent_time,
                 spent_time, status) -> None:
        self.connect()
        task = Task(
            board_id=board_id,
            title=title,
            description=description,
            author=author,
            assigned_to=assigned_to,
            published=published,
            finish_date=finish_date,
            planned_finish_date=planned_finish_date,
            planned_spent_time=planned_spent_time,
            spent_time=spent_time,
            status=status
        )
        self.session.add(task)
        self.session.commit()

    # Функция для запроса всех задач
    def get_task(self) -> list:
        self.connect()
        return self.session.query(Task).all()

    # Функция для добавления комментария
    def add_comment(self, task_id, author, text, published) -> None:
        self.connect()
        comment = Comment(
            task_id=task_id,
            author=author,
            text=text,
            published=published
        )
        self.session.add(comment)
        self.session.commit()

    # Функция для запроса всех комментариев
    def get_comment(self) -> list:
        self.connect()
        return self.session.query(Comment).all()

    # Функция для добавления доступа
    def add_access(self, board_id, user_id) -> None:
        self.connect()
        access = Access(
            board_id=board_id,
            user_id=user_id
        )
        self.session.add(access)
        self.session.commit()

    # Функция для запроса всех доступов
    def get_access(self) -> list:
        self.connect()
        return self.session.query(Access).all()  

db = DB(SQLALCHEMY_DATABASE_URI)

#db.add_user('Vasya12344', '<EMAIL14>', 'Vasya14', 'Pupkin14', 'Pupkovic14', 'Developer', 'user')
