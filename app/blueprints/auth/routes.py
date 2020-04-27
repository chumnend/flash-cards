from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.models import User
from app.blueprints.auth import bp
from app.blueprints.auth.forms import RegisterForm, LoginForm

# REGISTER ==========================================================
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for('main.index') )

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect( url_for('auth.login') )

    return render_template(
        'auth/register.html',
        form=form,
    )

# LOGIN =============================================================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('main.index') )

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Invalid username or password')
            return redirect( url_for('auth.login') )
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template(
        'auth/login.html',
        form=form,
    )

# LOGOUT ============================================================
@bp.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('main.index') )
