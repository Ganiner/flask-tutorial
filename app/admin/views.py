from . import admin
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required


@admin.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check(form.password.data):
                login_user(user)
                return redirect(url_for('admin.index'))
            else:
                flash("用户名或者密码错误")
                return redirect(url_for('admin.login'))
        else:
            flash('没有你这个用户，请注册')
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出了。')
    return redirect(url_for('admin.login'))


@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            flash('注册成功')
            return redirect(url_for('admin.login'))
        except:
            flash('帐号已存在')
            return redirect(url_for('admin.register'))
    return render_template('admin/register.html', form=form)
