from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # user id
    owner = db.Column(db.Integer)

    def __repr__(self):
        return '<Board {}>'.format(self.name)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user id
    author = db.Column(db.Integer)
    text = db.Column(db.String)
    published = db.Column(db.DateTime, nullable=False)
    task_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    text = db.Column(db.String)
    # user creator id
    author = db.Column(db.Integer)
    # user assignees id
    assigned_to = db.Column(db.Integer)
    published = db.Column(db.DateTime, nullable=False)
    finish_date = db.Column(db.DateTime)
    planned_finish_date = db.Column(db.DateTime)
    planned_spent_time = db.Column(db.Integer)
    # В часах
    spent_time = db.Column(db.Integer)
    board_id = db.Column(db.Integer)
    status = db.Column(db.String)

    def __repr__(self):
        return '<Task {}>'.format(self.name)

class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    board_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Access {}>'.format(self.id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    fist_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    patronymic = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(64), index=True, unique=True)
    position = db.Column(db.String(64), index=True, unique=False)
    role = db.Column(db.String(10), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    



