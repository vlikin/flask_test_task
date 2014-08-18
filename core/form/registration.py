from core.form.profile import ProfileForm
from wtforms import BooleanField, PasswordField, validators

class RegistrationForm(ProfileForm):
  password = PasswordField('New Password', [
      validators.Required(),
      validators.EqualTo('confirm', message='Passwords must match')
  ])
  confirm = PasswordField('Repeat Password')
  accept_tos = BooleanField('I accept the TOS', [validators.Required()])