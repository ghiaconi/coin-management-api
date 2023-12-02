from .base import db, Base, user_token, text
from datetime import datetime


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)  # TODO create admin only by verification(invitation only)
    password = db.Column(db.String(255), nullable=False)  # TODO add encryption
    archived_tokens_refs = db.Column(db.JSON, default=[])  # TODO move to the join table
    monitored_tokens_refs = db.Column(db.JSON, default=[])  # TODO move to the join table
    # Define the relationship to Token
    tokens = db.relationship('Token', secondary=user_token, backref='users')

    def assign_token(self, token):
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        patch = f'{{"{token.id}": "{current_timestamp}"}}'
        remove_query = text(
            f"UPDATE user SET archived_tokens_refs = JSON_REMOVE(archived_tokens_refs, '$.{token.id}') WHERE id = :user_id"
        )
        add_query = text(
            f"UPDATE user SET monitored_tokens_refs = JSON_MERGE_PATCH(monitored_tokens_refs, '{patch}') WHERE id = :user_id"
        )

        self.tokens.append(token)
        db.session.execute(add_query, {"user_id": self.id})
        db.session.execute(remove_query, {"user_id": self.id})
        db.session.commit()

    def unlink_token(self, token):
        patch = f'{{"{token.id}": "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"}}'
        remove_query = text(
            f"UPDATE user SET monitored_tokens_refs = JSON_REMOVE(monitored_tokens_refs, '$.{token.id}') WHERE id = :user_id"
        )
        add_query = text(
            f"UPDATE user SET archived_tokens_refs = JSON_MERGE_PATCH(archived_tokens_refs, '{patch}') WHERE id = :user_id"
        )

        db.session.execute(add_query, {"user_id": self.id})
        db.session.execute(remove_query, {"user_id": self.id})
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
            serialized_data['archived_tokens_ids'] = {
                'total_records': len(self.archived_tokens_refs),
                'data': self.archived_tokens_refs
            }
        if include_active_tokens:
            serialized_data['monitored_tokens_ids'] = {
                'total_records': len(self.monitored_tokens_refs),
                'data': self.monitored_tokens_refs
            }
        return serialized_data

    def __repr__(self):
        return f'<User {self.username}>'
