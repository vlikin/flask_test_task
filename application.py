"""
this is the "secret sauce" -- a single entry-point that resolves the
import dependencies.  If you're using blueprints, you can import your
blueprints here too.

then when you want to run your app, you point to main.py or `main.app`
"""
from app import app

import core.lib

# Views.
from core.views.index import Index
from core.views.login import Login
from core.views.remote import Remote
from core.views.music import Music
from core.views.registration import RegistrationView

# Routes.
app.add_url_rule('/', view_func=Index.as_view('home'), methods=['GET'])
app.add_url_rule('/<page>/', view_func=Index.as_view('index'), methods=['GET'])
app.add_url_rule('/login/', view_func=Login.as_view('login'), methods=['GET', 'POST'])
app.add_url_rule('/registration/', view_func=RegistrationView.as_view('registration'), methods=['GET', 'POST'])
app.add_url_rule('/remote/', view_func=Remote.as_view('remote'), methods=['GET', 'POST'])
app.add_url_rule('/music/', view_func=Music.as_view('music'), methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)