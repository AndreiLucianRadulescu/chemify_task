from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        validators=[InputRequired()],
    )
