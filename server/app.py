from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.get('/messages')
def messages():
    return [ m.to_dict() for m in Message.query.all() ], 200

@app.post('/messages')
def add_message():
    new_message = Message(
        body = request.json.get('body'),
        username = request.json.get('username')
        )
    db.session.add(new_message)
    db.session.commit()
    return new_message.to_dict()

@app.patch('/messages/<int:id>')
def messages_by_id(id):
    mess = Message.query.where(Message.id == id).first()
    if mess:
        for key in request.json.keys():
            setattr(mess,key,request.json[key])
        db.session.add(mess)
        db.session.commit()
        return mess.to_dict()
    return {message: "message not found."}, 404


@app.delete('/messages/<int:id>')
def delete_message(id):
    mess = Message.query.where(Message.id == id).first()
    if mess:
        db.session.delete(mess)
        return {}, 204
    else:
        return { 'error': 'Not found' }, 404

if __name__ == '__main__':
    app.run(port=5555)
