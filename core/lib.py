from app import app, db, login_manager
from core.model.user import UserModel
from core.model.friend import FriendModel

from flask import render_template
from flask.ext.login import current_user

@app.context_processor
def inject_user():
    return dict(user=current_user)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@login_manager.user_loader
def load_user(user_id):
  user = UserModel.query.filter(UserModel.id==user_id).first()
  return user

def init_db():
  db.drop_all()
  db.create_all()
  users = dict(
    admin = dict(
      obj = None,
      friends = dict(
        ask = [],
        confirm = ['viktor', 'elena']
      ),
      best_friend = 'viktor'
    ),
    viktor=dict(
      obj=None,
      friends = dict(
        ask = ['admin', 'elena'],
        confirm = []
      ),
      best_friend = 'elena'
    ),
    elena=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = ['viktor']
      ),
      best_friend = 'viktor'
    ),
    guest=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user1=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user2=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user3=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user4=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user5=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user6=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user7=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user8=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user9=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
    user10=dict(
      obj=None,
      friends = dict(
        ask = ['admin'],
        confirm = []
      )
    ),
  )
  # It creates users.
  for username, user in users.items():
    user['obj'] = UserModel.register(username, username + '@example.com', username)

  # It generates requests for friendship.
  for username, user in users.items():
    for friendname in user['friends']['ask']:
      friend = users[friendname]['obj']
      user['obj'].ask_for_friendship(friend)

  # It generates confirmations for friendship.
  for username, user in users.items():
    for friendname in user['friends']['confirm']:
      friend = users[friendname]['obj']
      user['obj'].confirm_friendship(friend)

  # It attaches the best friends.
  for username, user in users.items():
    if 'best_friend' not in user:
      continue
    best_friend = users[user['best_friend']]['obj']
    user['obj'].set_best_friend(best_friend)

  return db

def drop_all():
  import core.model.friend
  import core.model.user
  db.drop_all()