import flask.views
from app import db
from core.decorators import for_anonymous
from core.form.registration import RegistrationForm
from core.models.user import User
from flask import flash, request, redirect, render_template, url_for
from sqlalchemy import or_

class RegistrationView(flask.views.MethodView):
  @for_anonymous('index')
  def get(self):
    form = RegistrationForm()
    return render_template('registration.html', form=form)

  @for_anonymous('index')
  def post(self):
    form = RegistrationForm(request.form)
    if form.validate():
      missing = User.query.filter(or_(\
        User.username==form.username.data,\
        User.email==form.email.data,\
      )).first()
      if missing is not None:
        flash('A such user already exists.', 'error')
        return render_template('registration.html', form=form)

      user = User(form.username.data, form.email.data, form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Thanks for registering', 'info')
      return redirect(url_for('login'))
    return render_template('registration.html', form=form)