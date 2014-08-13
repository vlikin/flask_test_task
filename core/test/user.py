from core.test.base import BaseTestCase
from lxml.html import fromstring


class CoreTestCase(BaseTestCase):
  '''
    - It tests the core functionality.
  '''

  def test_login_page(self):
    '''
      - It tests the structrue of the login page.
    '''
    rv = self.app.get('/login/')
    doc = fromstring(rv.data)
    form = doc.cssselect('div.page form')[0]
    assert len(form.xpath('//input[@name="username"]')) == 1
    assert len(form.xpath('//input[@name="password"]')) == 1
    assert len(form.xpath('//input[@value="Login"]')) == 1

  def test_registration_page(self):
    '''
      - It tests the structrue of the user registration page.
    '''
    rv = self.app.get('/registration/')
    doc = fromstring(rv.data)
    form = doc.cssselect('div.page form')[0]
    assert len(form.xpath('//input[@name="username"]')) == 1
    assert len(form.xpath('//input[@name="email"]')) == 1
    assert len(form.xpath('//input[@name="password"]')) == 1
    assert len(form.xpath('//input[@name="confirm"]')) == 1
    assert len(form.xpath('//input[@name="accept_tos"]')) == 1
    assert len(form.xpath('//input[@value="Register"]')) == 1

  def test_user_process(self):
    '''
      - It tests the user registration process.
    '''
    rv = self.register({
      'username': 'username',
      'password': 'password',
      'email': 'username@domain.com'
    })
    assert 'Thanks for registering' in rv.data

    rv = self.login('username', 'password')
    assert 'Welcome again!' in rv.data

    rv = self.app.get('/logout/', follow_redirects=True)
    assert 'User went out.' in rv.data

  def test_friendship(self):
    '''
      - It tests friendship functionality these are hidden into UserModel.
    '''
    pass