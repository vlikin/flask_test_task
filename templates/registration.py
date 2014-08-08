{% extends "base.html" %}
{% block body %}
  <div class="page page-login">
    <h1>Welcome!</h1>
    {% if 'username' in session %}
      <p>Welcome back {{session['username']}}!</p>
      <form action="{{url_for('login')}}" method="post">
        <input type="submit" name="logout" value="Logout">
      </form>
    {% else %}
      <form action="{{url_for('login')}}" method="post">
        <p>Username: <br />
        <input type="text" name="username" /></p>
        <p>Password: <br />
        <input type="password" name="password" /></p>
        <p><input type="submit" name="login" value="Login" /></p>
      </form>
    {% endif %}
  </div>
{% endblock %}