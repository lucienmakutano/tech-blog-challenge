try:
    from blog_app import app, db, bcrypt
    from flask import render_template, redirect, request, flash, url_for
    from flask_login import login_required, login_user, logout_user
    from blog_app.forms import Login, Register
    from blog_app.model import Users
except ModuleNotFoundError:
    print('unable to load the modules')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if request.method == 'GET':
        return render_template('session/login.html', form=form)

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user)

            return redirect(url_for('home'))

        flash('email or password is incorrect')

    return render_template('session/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if request.method == 'GET':
        return render_template('session/register.html', form=form)

    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = Users(name=name, email=email, password=hash_password)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('home'))

    return render_template('session/register.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
