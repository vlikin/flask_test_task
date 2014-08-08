from functools import wraps
from flask import request, redirect, url_for, flash
from flask.ext.login import current_user

def for_anonymous(redirect_to='home'):
  def real_decorator(function):
    def wrapper(*args, **kwargs):
      print 'level 3'
      if current_user.is_authenticated():
        redirect_to = getattr(kwargs, 'redirect_to', 'home')
        flash('Sorry, you should not see pages for anonymous users.', 'warning')
        return redirect(url_for(redirect_to))
      return function(*args, **kwargs)
    return wrapper
  return real_decorator

def for_anonymous_1(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if current_user.is_authenticated():
      redirect_to = getattr(kwargs, 'redirect_to', 'home')
      flash('Sorry, you should not see pages for anonymous users.', 'warning')
      return f(*args, **kwargs)
      return redirect(url_for(redirect_to))
    return f(*args, **kwargs)
  return decorated_function