from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a string'
bootstrap = Bootstrap(app)
manager = Manager(app)


class NameForm(FlaskForm):
    name = StringField('你叫什么名字', validators=[Required()])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你更改了名字')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', name=session.get('name', None), form=form)


@app.route('/<username>')
def user(username):
    return render_template('user.html', name=username)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
