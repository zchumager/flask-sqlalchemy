from flask import Blueprint, request, jsonify
from sql.models import *

author_controller = Blueprint('author_controller', __name__)


@author_controller.route('/authors/', methods=['GET', 'POST'])
def create_author():
    if request.method == 'POST':
        request_body = request.get_json()

        author = Author(name=request_body.get('name'))
        session.add(author)
        session.commit()

        return jsonify(author_schema.dump(author))
    elif request.method == 'GET':
        return jsonify(author_schema.dump(session.query(Author).all(), many=True))


@author_controller.route('/authors/id/<author_id>')
def find_author_by_id(author_id):
    return jsonify(author_schema.dump(list(session.query(Author).filter(Author.id == author_id)), many=True))
