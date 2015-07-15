
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import os

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'
    token = Column(String(120), primary_key=True)

    def __init__(self, token):
        self.token = token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db = SQLAlchemy(app)

Base.query = db.session.query_property()

db.create_all()


db.session.add(Token(os.urandom(32).decode('unicode-escape')))
db.session.commit()

ts = Token.query.first()

print ts

