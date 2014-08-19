from app import db
from core.model.friend import FriendModel
from core.table.user import UserTable
from flask.ext.login import UserMixin
from sqlalchemy import func, or_, and_, case
from sqlalchemy.orm import aliased

class UserModel(UserTable, UserMixin):

  @staticmethod
  def delete_by_id(id):
    '''
      - It deletes a user by his id.
    '''
    UserModel.query.filter(UserModel.id==id).delete()
    FriendModel.query.filter(or_(FriendModel.user_id==id, FriendModel.friend_id)).delete()

  @staticmethod
  def load_by_id(user_id):
    '''
      - It loads a user by his id.
    '''
    return UserModel.query.filter(UserModel.id==user_id).first()

  @staticmethod
  def load_by_username(username):
    '''
      - It loads a user by his username.
    '''
    return UserModel.query.filter(UserModel.username==username).first()

  @staticmethod
  def register(username, email, password):
    '''
      - It registers a user into the system.
    '''
    user = UserModel(username, email, password)
    db.session.add(user)
    db.session.commit()
    return user

  @staticmethod
  def is_free(username, email):
    '''
      - It checks if a user is registered with a such data in the system.
    '''
    user = UserModel.query.filter(or_(\
      UserModel.username==username,\
      UserModel.email==email,\
    )).first()
    return user is None

  def set_best_friend(self, friend, commit=True):
    '''
      - It sets a best friend.
    '''
    if not self.is_friend(friend):
      raise Exception('He is not your friend. You can not set him as the best friend.')
    self.best_friend_id = friend.id
    db.session.add(self)
    db.session.commit()

  def deattach_best_friend(self, commit=True):
    '''
      - It deattachs the best friend.
    '''
    self.best_friend_id = None
    if commit:
      db.session.add(self)
      db.session.commit()


  def update_profile(self, profile=dict()):
    '''
      - It tries to update user's profile correctly.
    '''
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
    '''
      - It checks if the user is a friend.
    '''
    relation = FriendModel.query.filter(and_(FriendModel.user_id==self.id, FriendModel.friend_id==friend.id)).first()
    if relation is None:
      return None
    return relation.status


  def get_friends(self, page=1, per_page=2):
    '''
      - It returns a list of friends.
    '''
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
    '''
      - It returns a list of users with data.
    '''
    FUserModel = aliased(UserModel)
    query_1 = db\
      .session.query(
        UserModel.id,
        UserModel.username,
        UserModel.email,
        UserModel.best_friend_id,
        FUserModel.username.label('friend_username'),
        func.count().label('friends')
      )\
      .select_from(UserModel)\
      .outerjoin(FUserModel, UserModel.best_friend_id==FUserModel.id)\
      .outerjoin(FriendModel, and_(UserModel.id==FriendModel.user_id))\
      .group_by(FriendModel.user_id)
    s_1 = query_1.subquery('s_1')
    query_2 = db\
      .session.query(s_1, FriendModel.status)\
      .select_from(s_1)\
      .outerjoin(FriendModel, and_(FriendModel.user_id==s_1.c.id, FriendModel.friend_id==self.id))\
      .order_by(case([
        (s_1.c.id==self.id, 0),
        (FriendModel.status=='request', 1),
        (FriendModel.status=='decision', 2),
        (FriendModel.status=='confirmed', 3),
        (FriendModel.status=='accepted', 4),
      ], else_=99))\
      .limit(per_page + 1)\
      .offset((per_page - 1) * (page - 1))
    has_next = (query_2.count() == (per_page + 1))
    user_tuple_list = query_2.all()[:-1]
    user_dict_list = [ dict(zip(['id', 'username', 'email', 'best_friend_id', 'best_friend_username', 'count_friends', 'status'], user_tuple)) for user_tuple in user_tuple_list ]

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
