from app import app
from flask import redirect, url_for, flash
from flask.ext.classy import FlaskView
from flask.ext.login import login_required, logout_user

class LogoutView(FlaskView):
  @login_required
  def get(self):
    logout_user()
    flash('User went out.', 'info')
    return redirect(url_for('IndexView:get', page='home'))

LogoutView.register(app)