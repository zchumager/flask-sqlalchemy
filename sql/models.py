from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from marshmallow_sqlalchemy import ModelSchema

engine = create_engine("sqlite:///db.sql")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Author: {self.name}"


class AuthorSchema(ModelSchema):
    class Meta:
        model = Author


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", backref=backref("books"))

    def __repr__(self):
        return f"Book: {self.title}"


class BookSchema(ModelSchema):
    class Meta:
        model = Book


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean)
    secret_key = Column(String)

    def __repr__(self):
        return f"User: {self.username}"


class UserSchema(ModelSchema):
    class Meta:
        model = User


author_schema = AuthorSchema()
book_schema = BookSchema()
user_schema = UserSchema()

Base.metadata.create_all(engine)
