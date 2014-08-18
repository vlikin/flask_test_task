from wtforms import Form, BooleanField, TextField, PasswordField, validators

class ProfileForm(Form):
  username = TextField('Username', [validators.Length(min=4, max=25)])
  email = TextField('Email Address', [validators.Length(min=6, max=35)])
  password = PasswordField('New Password', [
      validators.EqualTo('confirm', message='Passwords must match')
  ])
  confirm = PasswordField('Repeat Password')