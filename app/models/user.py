from .base import db, Base, user_token


class User(Base):
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)  # TODO create admin only by verification(invitation only)
    password = db.Column(db.String(255), nullable=False)  # TODO add encryption
    archived_tokens_refs = db.Column(db.JSON)
    # Define the relationship to Token
    tokens = db.relationship('Token', secondary=user_token, backref='users')

    def assign_token(self, token):
        if self.archived_tokens_refs is not None and token.key in self.archived_tokens_refs:
            self.archived_tokens_refs.remove(token.key)

        self.tokens.append(token)
        db.session.commit()

    def unlink_token(self, token):
        if self.archived_tokens_refs is None:
            self.archived_tokens_refs = []

        self.archived_tokens_refs.append(token.key)
        self.tokens.remove(token)
        db.session.commit()

    def serialize(self, **kwargs):
        include_active_tokens = kwargs.get('include_active_tokens', False)
        include_archived_tokens = kwargs.get('include_archived_tokens', False)

        serialized_data = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        if include_archived_tokens:
            archived_refs = self.archived_tokens_refs or []
            serialized_data['archived_tokens_ids'] = {
                'total_records': len(archived_refs),
                'data': archived_refs
            }
        if include_active_tokens:
            tokens_data = [token.serialize() for token in self.tokens]
            serialized_data['monitored_tokens'] = {
                'total_records': len(tokens_data),
                'data': tokens_data
            }
        return serialized_data

    def __repr__(self):
        return f'<User {self.username}>'
