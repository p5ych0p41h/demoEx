# from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField, SelectField, StringField,
                     # TextAreaField, IntegerField, BooleanField, RadioField,
                     )
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.accounts.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField("Имя пользователя", validators=[DataRequired()])
    role = SelectField("Роль", choices=[('exp', 'Эксперт'), ('ope', 'Оператор по работе с экспертами'), ('adm', 'Администратор')])
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=4, max=45)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
