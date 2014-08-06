from core.context import get_db, get_login_manager

login_manager = get_login_manager()

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

def init_db():
  db = get_db()
  from core.models.user import User
  db.drop_all()
  db.create_all()
  admin = User('admin', 'admin@example.com', 'admin')
  guest = User('guest', 'guest@example.com', 'guest')
  db.session.add(admin)
  db.session.add(guest)
  db.session.commit()

  return db

def drop_all():
  db = get_db()
  from core.models.user import User
  db.drop_all()