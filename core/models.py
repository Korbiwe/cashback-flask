from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query

from core.utils import random_uuid4_as_hex

db = SQLAlchemy()


class QueryWithSoftDelete(Query):
    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)


class BaseModel(db.Model):
    __abstract__ = True

    query_class = QueryWithSoftDelete

    id = db.Column(db.String, primary_key=True, default=random_uuid4_as_hex,
                   unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, default=False)

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.deleted = True
        db.session.commit()

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name is not 'deleted' and
            c.name is not 'deleted_at'
        }
