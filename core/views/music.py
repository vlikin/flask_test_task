import flask, flask.views
from flask.ext.login import login_required
import os

class Music(flask.views.MethodView):
  def get(self):
    songs = os.listdir('static/files/music/')
    return flask.render_template('music.html', songs=songs)