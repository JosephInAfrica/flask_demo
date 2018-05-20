from flask import Flask, render_template, session, url_for, flash, redirect
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_script import Manager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a looooong string'

manager = Manager(app)

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    old_name = session.get('name') or "world"

    if form.validate_on_submit():
        session['name'] = form.name.data
        if session['name'] != old_name and old_name is not None:
            flash('looks like you have changed your name!')
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


if __name__ == '__main__':
    manager.run()
