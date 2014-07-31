import flask, flask.views
import os

class Index(flask.views.MethodView):

    def get(self, page='default'):
        tpl_path = 'templates/index/%s.html' % page
        if not os.path.isfile(tpl_path):
            tpl_name = 'index/default.html'
        else:
            tpl_name = 'index/%s.html' % page
        return flask.render_template(tpl_name)