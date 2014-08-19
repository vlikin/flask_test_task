from app import app, db
from core.form.profile import ProfileForm
from core.model.user import UserModel
from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import current_user, login_required
from flask.ext.classy import FlaskView

import pdb

class ProfileView(FlaskView):
  def get(self, id):
    user = UserModel.load_by_id(id)
    return render_template('profile/index.html', user=user)

  def index(self):
    return render_template('profile/index.html', user=current_user)

  @login_required
  def edit(self):
    form = ProfileForm(obj=current_user)
    return render_template('profile/edit.html', form=form)

  @login_required
  def post(self):
    form = ProfileForm(request.form)
    if form.validate():
      try:
        current_user.update_profile(dict(
          username = form.username.data,
          email = form.email.data
        ))
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been edited.')
      except Exception as e:
        flash(str(e), 'warning')

    return render_template('profile/edit.html', form=form)

  def view(self, user_id):
    user = UserModel.load_by_id(user_id)
    return render_template('profile/index.html', user=user)

  @login_required
  def make_best_friend(self, id):
    friend = UserModel.load_by_id(id)
    try:
      current_user.set_best_friend(friend)
      flash('%s is your best friend now.' % friend.username)
    except Exception as e:
      flash(str(e), 'warning')
    return redirect(url_for('ProfileView:list'))

  @login_required
  def ask_for_friendship(self, id):
    friend = UserModel.load_by_id(id)
    try:
      user_relation, friend_relation = current_user.ask_for_friendship(friend)
      if user_relation is not None:
        flash('The request for friendship has been sent.')
    except Exception as e:
      flash(str(e), 'warning')
    return redirect(url_for('ProfileView:list'))

  @login_required
  def confirm_friendship(self, id):
    friend = UserModel.load_by_id(id)
    try:
      current_user.confirm_friendship(friend)
      flash('Your friendship with "%s" has been confirmed.' % friend.username)
    except Exception as e:
      flash(str(e), 'error')
    return redirect(url_for('ProfileView:list'))

  @login_required
  def delete_friendship(self, id=None):
    friend = UserModel.load_by_id(id)
    current_user.delete_friendship(friend)
    flash('Your friendship with "%s" has been deleted.' % friend.username)
    return redirect(url_for('ProfileView:list'))

  @login_required
  def friends(self):
    page = int(request.args.get('page', '1'))
    friends, pagination = current_user.get_friends(page, 4)
    return render_template('profile/friends.html', user=current_user, friends=friends, pagination=pagination)

  @login_required
  def list(self):
    page = int(request.args.get('page', '1'))
    users, has_next = current_user.get_users(page, 4)

    return render_template('profile/list.html', users=users, has_next=has_next, page=page, pagination_view='ProfileView:list')

ProfileView.register(app)