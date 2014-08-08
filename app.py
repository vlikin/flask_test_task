from flask import Flask
from flask.ext.login import LoginManager

import settings

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_object(settings)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from core.views.login import Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if __name__ == '__main__':
  app.run(debug=True)
