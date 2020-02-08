# https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
#https://inneka.com/programming/python/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-same-thread/

from sql.models import *
from controllers.AuthorController import author_controller
from controllers.BookController import book_controller
from flask import Flask

app = Flask(__name__)
app.register_blueprint(author_controller)
app.register_blueprint(book_controller)


@app.teardown_request
def remove_session(ex=None):
    session.remove()


if __name__ == '__main__':
    app.run()
