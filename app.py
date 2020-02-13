# https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
# https://inneka.com/programming/python/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-same-thread/
# https://pythonprogramming.net/flask-email-tutorial/
# https://stackoverflow.com/questions/37058567/configure-flask-mail-to-use-gmail
# https://www.geeksforgeeks.org/generating-random-ids-using-uuid-python/
"""
Generate a Google Account Security Password for Flask Mail

    1. https://myaccount.google.com/security
    2. App Passwords
    3. Select app -> Mail
    4. Select device -> Other (Custom name)
    5. Generate
"""

from sql.models import *
from controllers.AuthorController import author_controller
from controllers.BookController import book_controller
from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_mail import Message
import uuid
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Controllers Registration
app.register_blueprint(author_controller)
app.register_blueprint(book_controller)

# Flask Mail Settings
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USE_SSL=True,
    MAIL_PORT=465,
    MAIL_USERNAME='pedro.machado@tala.co',
    MAIL_PASSWORD='klfsmfzzhngxyhci'  # Generated Password from Google Account Security
)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'secret-key-for-encryption'  # Change this!

mail = Mail(app)
jwt = JWTManager(app)


@app.route('/register_user/', methods=['POST'])
def register_user():
    request_body = request.get_json()
    recipient = request_body.get('recipient')
    generated_uuid = uuid.uuid1().hex

    msg = Message(
        "Welcome to our community",  # Message Title
        sender="pedro.machado@tala.co",
        recipients=[recipient]
    )
    msg.body = f'''Hi dear {recipient}
Welcome to our community please follow the next url to activate your account
http://127.0.0.1:5000/activate_account/{generated_uuid} '''

    try:
        user = User(username=recipient, password="password123", is_active=0, secret_key=generated_uuid)
        session.add(user)
        session.commit()

        mail.send(msg)

        return jsonify({'status': 'Mail sent successfully', 'secret_key': generated_uuid})
    except Exception:
        return jsonify({'status': 'Fail Process'})


@app.route('/activate_account/<generated_uuid>')
def activate_account(generated_uuid):
    user = session.query(User).filter(User.secret_key == generated_uuid).first()
    user.is_active = 1

    session.commit()

    return "Your Account has been activated"


@app.route('/generate_session/')
def generate_session():
    request_body = request.get_json()
    user = session.query(User).filter(
        User.username == request_body.get('username'),
        User.password == request_body.get('password'),
        User.is_active == True).first()

    if user is not None:
        # Decrypt identity
        access_token = create_access_token(identity=user.username)

        return jsonify(access_token=access_token)
    else:
        return "Session Not Generated"


@app.route('/users/')
@jwt_required
def list_users():
    current_user = get_jwt_identity()

    return jsonify(user_schema.dump(session.query(User).all(), many=True))


# Tear Down for SQL Alchemy
@app.teardown_request
def remove_session(ex=None):
    session.remove()


# Main function
if __name__ == '__main__':
    app.run()
