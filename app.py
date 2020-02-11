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

mail = Mail(app)


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


# Tear Down for SQL Alchemy
@app.teardown_request
def remove_session(ex=None):
    session.remove()


# Main function
if __name__ == '__main__':
    app.run()
