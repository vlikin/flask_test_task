import os
from app import app
from flask import render_template
from flask.ext.classy import FlaskView

class MusicView(FlaskView):
  def index(self):
    songs = os.listdir('static/files/music/')
    return render_template('music.html', songs=songs)

MusicView.register(app)