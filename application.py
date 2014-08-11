'''
  - It gets everything together.
'''
from app import app

import core.lib

import core.views.index
import core.views.login
import core.views.logout
import core.views.registration
import core.views.music
import core.views.profile

if __name__ == '__main__':
  app.run(debug=True)