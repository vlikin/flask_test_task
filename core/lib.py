from app import app, db, login_manager
from core.models.user import User

from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@login_manager.user_loader
def load_user(user_id):
  user = User.query.filter(User.id==user_id).first()
  return user

def init_db():
  db.drop_all()
  db.create_all()
  admin = User('admin', 'admin@example.com', 'admin')
  guest = User('guest', 'guest@example.com', 'guest')
  db.session.add(admin)
  db.session.add(guest)
  db.session.commit()

  return db

def drop_all():
  from core.models.user import User
  db.drop_all()