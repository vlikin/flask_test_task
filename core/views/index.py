import os
from app import app
from flask import render_template
from flask.ext.classy import FlaskView, route

class IndexView(FlaskView):
  def index(self):
    return self.get()

  def get(self, page='default'):
    tpl_path = 'templates/index/%s.html' % page
    if not os.path.isfile(tpl_path):
      tpl_name = 'index/default.html'
    else:
      tpl_name = 'index/%s.html' % page
    return render_template(tpl_name)

IndexView.register(app)