from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

from src import bcrypt, db
from src.accounts.models import User

from .forms import LoginForm, RegisterForm

accounts_bp = Blueprint("accounts", __name__)


# class MyModelView(sqla.ModelView):

#     def is_accessible(self):
#         return login.current_user.is_authenticated


# class MyAdminIndexView(admin.AdminIndexView):
#     @expose('/admin')
#     def index(self):
#         if not login.current_user.is_authenticated:
#             return redirect(url_for('.login_view'))
#         return super(MyAdminIndexView, self).index()


# admin = admin.Admin(app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')
# # Add view
# admin.add_view(MyModelView(User, db.session))

# @accounts_bp.route("/admin", methods=["GET", "POST"])
# def adm():
#     admin = Admin(app, name='microblog', template_mode='bootstrap3')
#     admin.add_view(ModelView(User, db.session))
#     admin.add_view(ModelView(Post, db.session))

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, name=form.name.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/check", methods=["GET", "POST"])
def check():
    if current_user.is_authenticated and current_user.role == "ope":
        flash("Вы оператор!", "success")
        return redirect(url_for("core.home"))


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))
