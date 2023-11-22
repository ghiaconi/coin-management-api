from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import DeclarativeBase


class Base(SQLAlchemy):
    def make_declarative_base(self, metadata=None):
        base = declarative_base(cls=DeclarativeBase, name='Model',
                                metadata=metadata, metaclass=DeclarativeMeta)
        base.query = self.session.query_property()
        return base


db = Base()
