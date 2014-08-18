from wtforms import Form, TextField, PasswordField, HiddenField, validators

class LoginForm(Form):
  username = TextField('Username', [validators.Required()])
  password = PasswordField('New Password', [validators.Required()])
  next = HiddenField()