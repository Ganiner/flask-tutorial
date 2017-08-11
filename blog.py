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
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# 我们要把数据库放在当下的文件夹,这个basedir就是当下文件夹的绝对路径

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(basedir, 'data.sqlite')
# 这里注意看，写的是URI（统一资源标识符）
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
# SQLALCHEMY_COMMIT_TEARDOWN 因为数据库每次有变动的时候，数据改变，但不会自动的去改变数据库里面的数据，
# 只有你去手动提交，告诉数据库要改变数据的时候才会改变，这里配置这个代表着，不需要你手动的去提交了，自动帮你提交了。
# 待会会有演示
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField('你叫什么名字', validators=[Required()])
    submit = SubmitField('提交')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 如果你学过数据库的话就知道我们一般通过id来作为主键，来找到对应的信息的,通过id来实现唯一性
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return 'users表: id为:{}, name为:{}'.format(self.id, self.name)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data)
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


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
