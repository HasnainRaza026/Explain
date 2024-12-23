from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'gvyf7y8uihj bf87y9iojk vg78y99ij0ok'
socketio = SocketIO(app)

class MessageForm(FlaskForm):
    message = StringField(label='', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/')
def home():
    form = MessageForm()
    return render_template('index.html', form=form)

@socketio.on('message')
def handle_message(data):
    with open("messages.txt", "a") as file:
        file.write(f"{data}\n")
    send(data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    try:
        with open("messages.txt", "r") as file:
            for line in file:
                send(line.strip())
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    socketio.run(app, debug=True)
