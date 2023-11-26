from .base import db, Base, user_token


class User(Base):
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)  # TODO create admin only by verification(invitation only)
    password = db.Column(db.String(255), nullable=False)  # TODO add encryption

    # Define the relationship to Token
    tokens = db.relationship('Token', secondary=user_token, backref='users')

    def serialize(self, include_tokens=False):
        serialized_data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        if include_tokens:
            serialized_data['tokens'] = [token.serialize() for token in self.tokens]
        return serialized_data

    def __repr__(self):
        return f'<User {self.username}>'
