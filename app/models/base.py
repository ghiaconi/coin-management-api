from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()


# Define the association tables
user_token = db.Table('user_token',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('token_id', db.String(60), db.ForeignKey('token.id')),
                      db.UniqueConstraint('user_id', 'token_id', name='uq_user_token')
                      )
