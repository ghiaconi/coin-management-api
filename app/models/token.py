from .base import db, Base


class Token(Base):
    key = db.Column(db.String(64), unique=True, nullable=False)
    attributes = db.Column(db.JSON)

    def __repr__(self):
        return f'<Token {self.key}>'
