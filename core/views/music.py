import flask, flask.views
from core.decorators import login_required
import os

class Music(flask.views.MethodView):

    @login_required
    def get(self):
        songs = os.listdir('static/files/music/')
        print songs
        return flask.render_template('music.html', songs=songs)