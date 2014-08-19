from app import db
from sqlalchemy.orm import relationship

class UserTable(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String)
  best_friend_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))

  best_friend = relationship('UserTable', backref='best_friend_of', remote_side='UserTable.id')
  user_friend = relationship('FriendTable', backref='user', foreign_keys='FriendTable.user_id')
  friend_user = relationship('FriendTable', backref='friend', foreign_keys='FriendTable.friend_id')

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

  def __repr__(self):
    return '<User id=%d username=%s email=%s best_friend_id=%s>' % (self.id, self.username, self.email, self.best_friend_id)