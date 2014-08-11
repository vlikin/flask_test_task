from app import app
from flask.ext.login import current_user
from flask import render_template
from flask.ext.classy import FlaskView

class ProfileView(FlaskView):
  def index(self):
    user = ''
    return render_template('profile.html', user=current_user)

ProfileView.register(app)