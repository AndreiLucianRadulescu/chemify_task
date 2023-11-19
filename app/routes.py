from app import app, db
from app.models import User
from app.forms import LoginForm
from werkzeug.security import generate_password_hash


from flask import (
    redirect,
    url_for,
    render_template,
    request,
    flash
)
from flask_login import (
    current_user,
    login_user,
    logout_user
)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template(
                "login.html",
                form=form,
                error_msg="Invalid username or password"
            )
        login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/home")
@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("home.html", username=current_user.username, tasks=current_user.tasks)
    
    form = LoginForm()
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template(
                "register.html",
                form=form,
                error_msg=True
            )
        
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration was successful! Please log in now.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=form)