from app import db
from core.table.user import UserTable

class FriendTable(db.Model):
  TYPES = [
    (u'request', u'Request'),# When an user ask for a friendship. So he request a friendship.
    (u'decision', u'Desicion'), # An user has received a request to get a friendship. He still desides.
    (u'confirmed', u'Confirmed'), # An user confirms the request to get a frienship.
    (u'accepted', u'Accepted'), # When an user's request is accepted.
  ]

  __table_args__ = (
    db.UniqueConstraint('user_id', 'friend_id', name='friendship'),
  )

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey(UserTable.id), nullable=False)
  friend_id = db.Column(db.Integer, db.ForeignKey(UserTable.id), nullable=False)
  status = db.Column(db.String, nullable=False)

  def __init__(self, user_id, friend_id, status):
    self.user_id = user_id
    self.friend_id = friend_id
    self.status = status

  def __repr__(self):
    return '<Friend id=%d user_id=%d friend_id=%d status=%s>' % (self.id, self.user_id, self.friend_id, self.status)