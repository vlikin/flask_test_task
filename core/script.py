from core.context import get_script_manager
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
  UserModel.delete(Usermodel.id==id)
  print 'The user with id=%d has been deleted.' % id

@script_manager.command
def check_query():
  '''
    - It creates the initial database.
  '''
  from core.model.user import UserModel
  from core.model.friend import FriendModel
  from sqlalchemy import or_, and_, func
  from app import db

  query_1 = db\
    .Query([UserModel, func.count(FriendModel.friend_id).label('friends')])\
    .select_from(UserModel)\
    .outerjoin(FriendModel, and_(UserModel.id==FriendModel.user_id))\
    .group_by(FriendModel.user_id)
  s_1 = query_1.subquery('s_1')

  query_2 = db\
    .session.query(s_1, FriendModel.status)\
    .select_from(s_1)\
    .join(FriendModel, FriendModel.user_id==s_1.c.id)

  user_tuple_list = query_2.all()
  user_dict_list = [ dict(zip(['id', 'username', 'email', 'password', 'friends_count', 'status'], user_tuple)) for user_tuple in user_tuple_list ]
  print user_dict_list[5]

  #print db.query(FriendModel).outerjoin(s, FriendModel.user_id==s.c.id)
  #query = db.session.query(FriendModel, s).outerjoin(s, FriendModel.user_id==s.c.id)
  print 'Hi!'