from app import app
from core.decorators import for_anonymous
from core.form.login import LoginForm
from core.model.user import UserModel
from flask import redirect, render_template, request, flash, url_for
from flask.ext.classy import FlaskView
from flask.ext.login import login_user
from sqlalchemy import or_

class LoginView(FlaskView):
  @for_anonymous('IndexView:get', 'home')
  def get(self):
    next = request.args.get('next', None)
    if next is None:
      next = url_for('IndexView:get', page='home')
    form_data = {
      'next': next
    }

    form = LoginForm(data=form_data)
    return render_template('login.html', form=form)

  @for_anonymous('IndexView:get', 'home')
  def post(self):
    form = LoginForm(request.form)
    if form.validate():
      user = UserModel.query.filter(
        UserModel.username==form.username.data,\
        UserModel.password==form.password.data,\
      ).first()
      if user is None:
        flash('Wrong authentication data.', 'error')
        return render_template('login.html', form=form)
      login_user(user)
      flash('Welcome again!', 'info')
      if form.next.data is None:
        return redirect(url_for('IndexView:get', page='home'))
      else:
        return redirect(form.next.data)
    return render_template('login.html', form=form)

LoginView.register(app)