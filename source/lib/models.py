from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    email = Column(String(64), index=True, unique=True)
    first_name = Column(String(64), index=True, unique=False)
    last_name = Column(String(64), index=True, unique=False)
    patronymic = Column(String(64), index=True, unique=False)
    position = Column(String(64), index=True, unique=False)
    role = Column(String(10), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.login)


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer(), primary_key=True)
    title = Column(String(64))
    # user id
    owner = Column(Integer, ForeignKey(User.id))

    def __repr__(self):
        return '<Board {}>'.format(self.title)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey(Board.id))
    title = Column(String(64))
    description = Column(String)
    # user id
    author = Column(Integer, ForeignKey(User.id))
    # user id
    assigned_to = Column(Integer, ForeignKey(User.id))
    published = Column(Date, nullable=False)
    finish_date = Column(Date)
    planned_finish_date = Column(Date)
    planned_spent_time = Column(Integer)
    # В часах
    spent_time = Column(Integer)
    status = Column(String)

    def __repr__(self):
        return '<Task {}>'.format(self.title)


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey(Task.id))
    # user id
    author = Column(Integer, ForeignKey(User.id))
    text = Column(String)
    published = Column(Date, nullable=False)

    def __repr__(self):
        return '<Comment {}>'.format(self.id)


class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey(Board.id))
    user_id = Column(Integer, ForeignKey(User.id))

    def __repr__(self):
        return '<Access {}>'.format(self.id)
