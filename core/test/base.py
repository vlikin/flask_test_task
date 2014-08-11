from app import app
from core.lib import init_db
from unittest import TestCase

import os
import tempfile


class BaseTestCase(TestCase):
  '''
    - It is a base TestCase class for the current project.
  '''

  def setUp(self):
    '''
      - It prepares tests.
    '''
    self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    self.app = app.test_client()
    init_db()

  def tearDown(self):
    '''
      - It clears traces after the execution of tests.
    '''
    os.close(self.db_fd)
    os.unlink(app.config['DATABASE'])

  def login(self, username, password):
    '''
      - It logins an user to the system.
    '''
    return self.app.post('/login/', data=dict(
      username=username,
      password=password,
    ), follow_redirects=True)

  def register(self, user):
    '''
      - It registeres an user to the system.
    '''
    return self.app.post('/registration/', data=dict(
      username=user['username'],
      password=user['password'],
      confirm=user['password'],
      email=user['email'],
      accept_tos=1
    ), follow_redirects=True)