from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_


from sqlalchemy.exc import OperationalError, NoSuchModuleError

from lib.models import User, Board, Task, Comment, Access
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import current_user

class DBError(Exception):
    """Ошибка работы с БД"""


class DB():
    def __init__(self, URL: str) -> None:
        self.URL = URL
        self.session = None
        self.engine = None
        self.base = None
        self.connection = None

    def connect(self) -> object:
        try:
            if self.connection is None:
                self.engine = create_engine(self.URL)
                self.connection = self.engine.connect()

        except OperationalError:
            raise DBError('Ошибка в логине, пароле или адресе БД')
        except NoSuchModuleError:
            raise DBError('Не правильно задан модуль БД')

    def create_session(self) -> None:
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def __repr__(self) -> str:
        return '<DB {}>'.format(self.URL)


class User_DB(DB):
    def __init__(self, URL: str):
        super().__init__(URL)
        self.login = None
        self.email = None
        self.password = None
        self.first_name = None
        self.last_name = None
        self.patronymic = None
        self.position = None
        self.role = None

    # Функция для добавления пользователя в БД
    def add_user(
        self,
        login: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        patronymic: str,
        position: str,
        role: str
    ) -> None:
        self.connect()
        self.create_session()
        hash_password = self.set_password(password)
        user = User(
            login=login,
            email=email,
            password=hash_password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            position=position,
            role=role,
        )
        self.session.add(user)
        self.session.commit()
        self.session.close()

    # Функция для получения пользователя по id
    def get_user(self, user_id: int) -> object:
        self.connect()
        self.create_session()
        user = self.session.query(User).filter(User.id == user_id).first()
        self.session.close()
        return user

    # Функция для превращения пароля в хеш
    def set_password(self, password):
        return generate_password_hash(password, method='pbkdf2:sha256:600000')

    # Функция для сравнения пароля с хеш паролем из БД
    def check_password(self, true_password, password):
        return check_password_hash(true_password, password)

    # Функция для проверки пользователя
    def validate_user(self, login: str, password: str) -> list:
        self.connect()
        self.create_session()
        user = self.session.query(User).filter(User.login == login).first()
        self.session.close()
        if user:
            if check_password_hash(user.password, password):
                return user
            else:
                return None

    # Функция для подсчета пользователей с одинаковым логином
    def login_counter(self, login: str) -> int:
        self.connect()
        self.create_session()
        login_count = self.session.query(User)\
            .filter(User.login == login)\
            .count()
        self.session.close()
        return login_count

    # Функция для подсчета пользователей с одинаковым email
    def email_counter(self, email: str) -> int:
        self.connect()
        self.create_session()
        email_count = self.session.query(User)\
            .filter(User.email == email)\
            .count()
        self.session.close()
        return email_count


class Board_DB(DB):
    # Функция для добавления доски
    def add_board(
        self,
        title: str,
        owner: int
    ) -> None:
        self.connect()
        self.create_session()
        board = Board(
            title=title,
            owner=owner
        )
        self.session.add(board)
        self.session.commit()
        self.session.close()

    # Функция для запроса доски
    def get_board(self, id: int) -> list:
        self.connect()
        self.create_session()
        self.get_query = self.session.query(Board).get(id)
        # извлекаем название доски
        self.board_title = self.get_query.title
        self.session.close()
        return self.board_title

    # Функция для запроса всех досок
    def get_boards(self) -> list:
        self.connect()
        self.create_session()
        get_query = self.session.query(
            Board.__table__,
            User.first_name,
            User.last_name)\
            .join(User, Board.owner == User.id)\
            .join(
                Access,
                and_(Access.board_id == Board.id,
                     Access.user_id == current_user.id)
            )\
            .order_by(Board.title)\
            .all()
        self.session.close()
        return get_query


class Task_DB(DB):
    # Функция для добавления задачи
    def add_task(
        self,
        board_id: int,
        title: str,
        description: str,
        author: int,
        assigned_to: int,
        published: str,
        finish_date: str,
        planned_finish_date: str,
        planned_spent_time: str,
        spent_time: int,
        status: str
     ) -> None:
        self.connect()
        self.create_session()
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
        self.session.close()

    # Функция для запроса всех задач
    def get_tasks(self) -> list:
        self.connect()
        self.create_session()
        user_tasks = self.session.query(Task)\
            .join(Board, Task.board_id == Board.id)\
            .join(Access, and_(
                Access.board_id == Board.id,
                Access.user_id == current_user.id)
            )\
            .all()
        self.session.close()
        return user_tasks


class Comment_DB(DB):
    # Функция для добавления комментария
    def add_comment(
        self,
        task_id: int,
        author: int,
        text: str,
        published: str
    ) -> None:
        self.connect()
        self.create_session()
        comment = Comment(
            task_id=task_id,
            author=author,
            text=text,
            published=published
        )
        self.session.add(comment)
        self.session.commit()
        self.session.close()

    # Функция для запроса всех комментариев
    def get_comment(self) -> list:
        self.connect()
        return self.session.query(Comment).all()


class Access_DB(DB):
    # Функция для добавления доступа
    def add_access(
        self,
        board_id: int,
        user_id: int
    ) -> None:
        self.connect()
        self.create_session()
        access = Access(
            board_id=board_id,
            user_id=user_id
        )
        self.session.add(access)
        self.session.commit()
        self.session.close()

    # Функция для запроса всех доступов
    def get_access(self) -> list:
        self.connect()
        return self.session.query(Access).all()
