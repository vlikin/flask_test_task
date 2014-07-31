from flask import Flask
import settings

# Views.
from core.views.index import Index
from core.views.login import Login
from core.views.remote import Remote
from core.views.music import Music

app = Flask(__name__)
app.secret_key = settings.secret_key

# Routes.
app.add_url_rule('/<page>/', view_func=Index.as_view('index'), methods=['GET'])
app.add_url_rule('/login/', view_func=Login.as_view('login'), methods=['GET', 'POST'])
app.add_url_rule('/remote/', view_func=Remote.as_view('remote'), methods=['GET', 'POST'])
app.add_url_rule('/music/', view_func=Music.as_view('music'), methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)