from core.context import get_script_manager
from sqlalchemy.orm import aliased
import core.lib as lib

import pdb

script_manager = get_script_manager()

@script_manager.command
def drop_all():
  '''It drops all tables.'''
  lib.drop_all()

@script_manager.command
def init_db():
  '''It creates the initial database.'''
  lib.init_db()

@script_manager.command
def delete_user(id):
  from core.model.user import UserModel
  UserModel.delete_by_id(id)
  print 'The user with id=%s has been deleted.' % id

@script_manager.command
def check_query():
  '''
    - It creates the initial database.
  '''
  from core.model.user import UserModel
  from core.model.friend import FriendModel
  from sqlalchemy import or_, and_, func, case
  from app import db

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
    .outerjoin(FriendModel, and_(FriendModel.user_id==s_1.c.id, FriendModel.friend_id==8))\
    .order_by(s_1.c.username)\
    .order_by(case([
      (FriendModel.status=='request', 0),
      (FriendModel.status=='confirmed', 1),
    ], else_=99))\

  user_tuple_list = query_2.all()
  user_dict_list = [ dict(zip(['id', 'username', 'email', 'best_friend_id', 'best_friend_username', 'friends_count', 'status'], user_tuple)) for user_tuple in user_tuple_list ]
  user_dict_list = [ (u['username'], u['best_friend_username'], u['best_friend_id']) for u in user_dict_list]
  print user_dict_list