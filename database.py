# SQLAlchemy is an ORM(Object Relational Mapping)
# Helps execute queris using methods
# Define the tablestructure is classes/models
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

# Map users table to User class
class User(Base):
    __tablename__ ="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    location: Mapped[str]=mapped_column(String(100))

# from flask_sqlalchemy import SQLAlchemy

# db=SQLAlchemy()

# class User(db.Model):
#     __tablename__='users'
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(50),nullable=False)
#     email=db.Column(db.String(120),unique=True,nullable=False)
#     password=db.Column(db.String(55),nullable=False)

