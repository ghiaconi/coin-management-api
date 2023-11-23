from .base import db, Base


class User(Base):
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
