from flask import Blueprint, request, jsonify
from sql.models import *

book_controller = Blueprint('book_controller', __name__)


@book_controller.route('/books/', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        request_body = request.get_json()

        book = Book(title=request_body.get('title'), author_id=request_body.get('author'))
        session.add(book)
        session.commit()

        return jsonify(book_schema.dump(book))
    elif request.method == 'GET':
        return jsonify(book_schema.dump(session.query(Book).all(), many=True))