from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'hguhjkbjv bjguhijkbnjbhguyfguihij nhguihkkjbnjuguih'

class MessageForm(FlaskForm):
    message = StringField(label='', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = MessageForm()
    messages = []
    
    if form.validate_on_submit():
        with open("messages.txt", "a") as file:
            file.write(f"{form.message.data}\n")
        
        return redirect('/')

    try:
        with open("messages.txt", "r") as file:
            messages = file.readlines()
    except FileNotFoundError:
        pass

    return render_template('index.html', form=form, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
