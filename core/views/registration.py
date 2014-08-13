from app import app, db
from core.decorators import for_anonymous
from core.form.registration import RegistrationForm
from core.model.user import UserModel
from flask import flash, request, redirect, render_template, url_for
from flask.ext.classy import FlaskView

class RegistrationView(FlaskView):
  @for_anonymous('IndexView:get', 'home')
  def get(self):
    form = RegistrationForm()
    return render_template('registration.html', form=form)

  @for_anonymous('IndexView:get', 'home')
  def post(self):
    form = RegistrationForm(request.form)
    if form.validate():
      is_free = UserModel.is_free(form.username.data, form.email.data)
      if not is_free:
        flash('A such user already exists.', 'error')
        return render_template('registration.html', form=form)

      user = UserModel.register(form.username.data, form.email.data, form.password.data)
      flash('Thanks for registering', 'info')
      return redirect(url_for('LoginView:get'))
    return render_template('registration.html', form=form)

RegistrationView.register(app)