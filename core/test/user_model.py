from core.model.user import UserModel
from core.test.base import BaseTestCase
from lxml.html import fromstring


class UserModelTestCase(BaseTestCase):
  '''
    - It tests the core functionality.
  '''
  test_user_data = dict(
    username='test_user_username',
    email='test_user_email@example.com',
    password='test_user_password'
  )
  test_user = None

  def test_relations(self):
    '''
      - It tests the model - UserModel. It checks the user process on the model level.
    '''
    # User is free.
    is_free = UserModel.is_free(self.test_user_data['username'], self.test_user_data['email'])
    assert is_free == True

    # Registers a user into the system.
    self.test_user = UserModel.register(\
      self.test_user_data['username'],\
      self.test_user_data['email'],\
      self.test_user_data['password']
    )
    assert self.test_user.username == self.test_user_data['username']
    assert self.test_user.email == self.test_user_data['email']

    # Logins in.
    rv = self.login(self.test_user_data['username'], self.test_user_data['password'])
    assert 'Welcome again!' in rv.data

    # Loads a friend.
    friend = UserModel.load_by_username('admin')
    assert friend.username == 'admin'

    # Checks it it is a friend. He is not a friend
    is_friend = self.test_user.is_friend(friend)
    assert is_friend == None # Checks it it is a friend. He is not a friend

    user_relation, friend_relation = self.test_user.ask_for_friendship(friend)
    assert user_relation.friend_id == friend_relation.user_id

    error_is = False
    try:
      self.test_user.ask_for_friendship(friend)
    except:
      error_is = True
    assert error_is == True # Checks it it is a friend. He is not a friend

    error_is = False
    try:
      self.test_user.confirm_friendship(friend)
    except:
      error_is = True
    assert error_is == True # Checks it it is a friend. He is not a friend

    is_friend = self.test_user.is_friend(friend)
    assert is_friend == 'request' # An user sent a request for frind

    is_friend = friend.is_friend(self.test_user)
    assert is_friend == 'decision' # An user received an invitation. It makes a decision.

    friend_relation, user_relation = friend.confirm_friendship(self.test_user)
    assert friend_relation.friend_id == user_relation.user_id # A friend confirms for a request for friendship.

    is_friend = self.test_user.is_friend(friend)
    assert is_friend == 'confirmed' # His request for friendship has been confirmed.

    is_friend = friend.is_friend(self.test_user)
    assert is_friend == 'accepted' # A friend accepted a request for friendship.

    # Check the best frined functionality.
    self.test_user.set_best_friend(friend)
    assert self.test_user.best_friend_id == friend.id # It sets the best friend.

    self.test_user.deattach_best_friend()
    assert self.test_user.best_friend_id == None # It deattaches the best frined.

    # Checks the relation deletion.
    friend.delete_friendship(self.test_user)
    status = self.test_user.is_friend(friend)
    assert status is None # A relation does not exist.

    UserModel.delete_by_id(self.test_user.id)
    self.test_user = UserModel.load_by_username(self.test_user_data['username'])
    assert self.test_user is None # A user does not exist.
