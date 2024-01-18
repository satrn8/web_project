from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.exc import OperationalError, NoSuchModuleError

from source.lib.models import User, Board, Task, Comment, Access


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

    # Функция для добавления пользователя
    def add_user(
        self,
        login: str,
        email: str,
        fist_name: str,
        last_name: str,
        patronymic: str,
        position: str,
        role: str
    ) -> None:
        self.connect()
        self.create_session()
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
        self.session.close()

    # Функция для запроса всех пользователей
    def get_users(self) -> list:
        self.connect()
        return self.session.query(User).all()

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

    # Функция для запроса всех досок
    def get_boards(self) -> list:
        self.connect()
        self.create_session()
        get_query = self.session.query(
            Board.__table__,
            User.first_name,
            User.last_name)\
            .join(User, Board.owner == User.id)\
            .order_by(Board.title)\
            .all()
        self.session.close()
        return get_query

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
    def get_task(self) -> list:
        self.connect()
        return self.session.query(Task).all()

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
