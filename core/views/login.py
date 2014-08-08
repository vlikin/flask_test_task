import flask.views
from flask import redirect, render_template, request, flash, url_for

from core.decorators import for_anonymous
from core.form.login import LoginForm
from core.models.user import User
from flask.ext.login import login_user
from sqlalchemy import or_

class Login(flask.views.MethodView):
  @for_anonymous('index')
  def get(self):
    form = LoginForm()
    return render_template('login.html', form=form)

  @for_anonymous('index')
  def post(self):
    form = LoginForm(request.form)
    if form.validate():
      user = User.query.filter(or_(\
        User.username==form.username.data,\
        User.password==form.password.data,\
      )).first()
      if user is None:
        flash('Wrong authentication data.', 'error')
        return render_template('login.html', form=form)

      login_user(user)
      return redirect(url_for('home'))