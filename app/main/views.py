from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from . import main
from .forms import NameForm
from ..models import User
from .. import db


@main.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
        # 这里注意一下,我们这里要写main.index,因为我们这个视图函数隶属于main这个蓝本,
        # main.index是他完整的名字.
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
