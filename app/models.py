import re
from hashlib import sha512

from . import app, db
import time


class Vote(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    ts = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    class_ = db.Column(db.Integer, nullable=False)
    pob = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    choice = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    def get_hfts(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.ts))

    def validate(self):
        conditions = [
            len(self.id) > 3,
            self.ts,
            len(self.name),
            len(self.pob),
            len(self.dob),
            len(self.gender),
            len(self.status),
            self.class_ < len(app.config['CLASSES']),
            self.class_ >= 0,
            self.choice < len(app.config['CANDIDATES']),
            self.choice >= 0,
        ]
        for cond in conditions:
            if not cond:
                breakpoint()
                return False
        return True


class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @classmethod
    def get(cls, key):
        field = app.config['PREFERENCES_FIELDS'].get(key)
        if not field:
            raise KeyError
        row = cls.query.filter_by(key=key).first()
        if not row:
            value = field[0](field[1])
            cls.set(key, value)
            return value
        return field[0](row.value)

    @classmethod
    def set(cls, key, value):
        field = app.config['PREFERENCES_FIELDS'].get(key)
        if not field:
            raise KeyError
        row = cls.query.filter_by(key=key).first()
        if not row:
            row = cls()
            row.key = key
            row.value = field[0](value)
            db.session.add(row)
        else:
            row.value = field[0](value)
        db.session.commit()

    @classmethod
    def delete(cls, key):
        if not app.config['PREFERENCES_FIELDS'].get(key):
            raise KeyError
        row = cls.query.filter_by(key=key).first()
        if not row:
            return
        db.session.delete(row)
        db.session.commit()


db.create_all()

db = db
