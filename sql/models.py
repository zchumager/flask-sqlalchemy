from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
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
        return "<Author(name={self.name!r})>".format(self=self)


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
        return "<Book(title={self.title!r})>".format(self=self)


class BookSchema(ModelSchema):
    class Meta:
        model = Book


author_schema = AuthorSchema()
book_schema = BookSchema()

Base.metadata.create_all(engine)
