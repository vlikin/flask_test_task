from app import app
from flask import render_template, request
from flask.ext.login import current_user, login_required
from flask.ext.classy import FlaskView
from flask.ext.pagination import Pagination

class ProfileView(FlaskView):
  @login_required
  def index(self):
    return render_template('profile/index.html', user=current_user)

  @login_required
  def friends(self):
    page = int(request.args.get('page', '1'))
    friends, pagination = current_user.get_friends(page, 4)
    return render_template('profile/friends.html', user=current_user, friends=friends, pagination=pagination)

ProfileView.register(app)