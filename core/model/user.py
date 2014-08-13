from app import db
from core.model.friend import FriendModel
from core.table.user import UserTable
from flask.ext.login import UserMixin
from sqlalchemy import func, or_

class UserModel(UserTable, UserMixin):
  @staticmethod
  def register(username, email, password):
    user = UserModel(username, email, password)
    db.session.add(user)
    db.session.commit()
    return user

  @staticmethod
  def is_free(username, email):
    user = UserModel.query.filter(or_(\
      UserModel.username==username,\
      UserModel.email==email,\
    )).first()
    return user is None

  def get_friends(self, page=1, per_page=2):
    friends = []
    paginator = UserModel.query.add_column(func.count(FriendModel.friend_id)).outerjoin(FriendModel, UserModel.id==FriendModel.friend_id).group_by(UserModel.id).paginate(page, per_page)
    for item in paginator.items:
      user = item[0]
      user.count_friends = item[1]
      friends.append(user)
    return friends, paginator


    '''
      ! Cool, but not productive.
      friends = []
      for relation in self.user_friend:
        friends.append(relation.user)
      return friends
    '''

  def ask_for_friendship(self, friend):
    '''
      - The user asks an user for the friendship.
    '''
    user_relation = FriendModel(self.id, friend.id, 'request')
    friend_relation = FriendModel(friend.id, self.id, 'decision')
    db.session.add(user_relation)
    db.session.add(friend_relation)
    db.session.commit()
    return user_relation, friend_relation

  def confirm_friendship(self, friend):
    '''
      - The user confirms a request for the friendship.
    '''
    user_relation = FriendModel.query.filter(\
      FriendModel.user_id==self.id,\
      FriendModel.friend_id==friend.id\
    ).first()
    if user_relation is None:
      # There is not a relation.
      return None
    if user_relation.status != 'decision':
      raise Exception('This relation could not be confirmed!')
    friend_relation = FriendModel.query.filter(\
      FriendModel.user_id==friend.id,\
      FriendModel.friend_id==self.id\
    ).first()
    user_relation.status = 'accepted'
    friend_relation.status = 'confirmed'
    db.session.add(user_relation)
    db.session.add(friend_relation)
    db.session.commit()
    return user_relation, friend_relation
