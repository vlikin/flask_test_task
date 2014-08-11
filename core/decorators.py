from functools import wraps
from flask import request, redirect, url_for, flash
from flask.ext.login import current_user

def for_anonymous(redirect_to='IndexView:get', page='home'):
  def real_decorator(function):
    def wrapper(*args, **kwargs):
      if current_user.is_authenticated():
        flash('Sorry, you should not see pages for anonymous users.', 'warning')
        return redirect(url_for(redirect_to, page=page))
      return function(*args, **kwargs)
    return wrapper
  return real_decorator