from app import db
from core.model.friend import FriendModel
from core.table.user import UserTable
from flask.ext.login import UserMixin
from sqlalchemy import func, or_, and_

class UserModel(UserTable, UserMixin):

  @staticmethod
  def delete_by_id(id):
    UserModel.query.filter(UserModel.id==id).delete()
    FriendModel.query.filter(or_(FriendModel.user_id==id, FriendModel.friend_id)).delete()

  @staticmethod
  def load_by_id(user_id):
    return UserModel.query.filter(UserModel.id==user_id).first()

  @staticmethod
  def load_by_username(username):
    return UserModel.query.filter(UserModel.username==username).first()

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

  def update_profile(self, profile=dict()):
    if 'username' in profile and self.username != profile['username']:
      user_username = UserModel.query.filter(UserModel.username==profile['username'], UserModel.username!=self.username).first()
      if user_username != None:
        raise Exception('A such username is used.')
    if 'email' in profile and self.email != profile['email']:
      user_email = UserModel.query.filter(UserModel.email==profile['email'], UserModel.email!=self.email).first()
      if user_email != None:
        raise Exception('A such email is used.')

    if 'password' in profile and profile['password']=='':
      del(profile['password'])

    for key in profile:
      setattr(self, key, profile[key])

  def is_friend(self, friend):
    relation = FriendModel.query.filter(and_(FriendModel.user_id==self.id, FriendModel.friend_id==friend.id)).first()
    if relation is None:
      return None
    return relation.status


  def get_friends(self, page=1, per_page=2):
    friends = []
    friends_subquery = db.Query(FriendModel.friend_id).select_from(FriendModel).filter(FriendModel.user_id==self.id)
    paginator = UserModel.query\
      .add_column(func.count(FriendModel.friend_id))\
      .outerjoin(FriendModel, and_(UserModel.id==FriendModel.user_id))\
      .group_by(FriendModel.user_id)\
      .having(UserModel.id.in_(friends_subquery))\
      .paginate(page, per_page)

    for item in paginator.items:
      user = item[0]
      user.count_friends = item[1]
      friends.append(user)
    return friends, paginator

  def get_users(self, page=1, per_page=2):
    query_1 = db\
      .session.query(UserModel.id, UserModel.username, func.count().label('friends'))\
      .select_from(UserModel)\
      .outerjoin(FriendModel, UserModel.id==FriendModel.user_id)\
      .group_by(UserModel.id)
    s_1 = query_1.subquery('s_1')
    query_2 = db\
      .session.query(s_1, FriendModel.status)\
      .select_from(s_1)\
      .outerjoin(FriendModel, and_(FriendModel.user_id==s_1.c.id, FriendModel.friend_id==self.id))\
      .limit(per_page + 1)\
      .offset((per_page - 1) * page)
    has_next = (query_2.count() == (per_page + 1))
    user_tuple_list = query_2.all()[:-1]
    user_tuple_list
    user_dict_list = [ dict(zip(['id', 'username', 'count_friends', 'status'], user_tuple)) for user_tuple in user_tuple_list ]
    return user_dict_list, has_next

  def ask_for_friendship(self, friend):
    '''
      - The user asks an user for the friendship.
    '''
    friend_relation = FriendModel.query.filter(\
      FriendModel.user_id==self.id,\
      FriendModel.friend_id==friend.id\
    ).first()
    if friend_relation is not None:
      raise Exception('The relation(user_id=%d, friend_id=%d) already exists with the status - "%s" ' % (self.id, friend.id, friend_relation.status))
    user_relation = FriendModel(self.id, friend.id, 'request')
    friend_relation = FriendModel(friend.id, self.id, 'decision')
    db.session.add(user_relation)
    db.session.add(friend_relation)
    db.session.commit()
    return user_relation, friend_relation

  def delete_friendship(self, friend):
    '''
      - It deletes the friendship.
    '''
    user_relation = FriendModel.query.filter(\
      FriendModel.user_id==self.id,\
      FriendModel.friend_id==friend.id\
    ).first()
    friend_relation = FriendModel.query.filter(\
      FriendModel.user_id==friend.id,\
      FriendModel.friend_id==self.id\
    ).first()
    db.session.delete(user_relation)
    db.session.delete(friend_relation)
    db.session.commit()

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
