# SQLAlchemy is an ORM(Object Relational Mapping)
# Helps execute queris using methods
# Define the tablestructure is classes/models
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Integer,DateTime,ForeignKey


class Base(DeclarativeBase):
    pass

# Map users table to User class
class Employee(Base):
    __tablename__ ="employees"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    location: Mapped[str]=mapped_column(String(100))
    age: Mapped[int]=mapped_column()


class Authentication(Base):
    __tablename__="user_authentication"
    id: Mapped[int]=mapped_column(primary_key=True)
    full_name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(DateTime)


# from flask_sqlalchemy import SQLAlchemy

# db=SQLAlchemy()

# class User(db.Model):
#     __tablename__='users'
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(50),nullable=False)
#     email=db.Column(db.String(120),unique=True,nullable=False)
#     password=db.Column(db.String(55),nullable=False)

