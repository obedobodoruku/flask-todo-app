import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db, bcrypt
from app.models import User, Task
from flask_login import login_user, current_user, login_required, logout_user
from app.forms import RegistrationForm, LoginForm, CreateTaskform, UpdateAccountForm

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("account"))
    return render_template("home.html", title="Home page")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You have been Registered!. You can now Login")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("account")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("account"))
        else:
            flash("Your login was unsuccessful. Please check Email and Password")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))



@app.route("/account")
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first()
    image_file = url_for('static', filename='profile_pictures/' + user.image_file)
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("account.html", title="Account Page", tasks=user_tasks, user=user, image_file=image_file)


@app.route("/addtask", methods=["GET", "POST"])
@login_required
def create_task():
    form = CreateTaskform()
    if form.validate_on_submit():
        new_tasks = Task(todo=form.task.data, description=form.description.data, user_id=current_user.id)
        db.session.add(new_tasks)
        db.session.commit()
        flash("Your Task has successfully been added")
        return redirect(url_for("account"))
    return render_template("create_task.html", title="New Task", form=form)



@app.route("/update<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    if current_user.is_authenticated:
        task = Task.query.get_or_404(task_id)
        form = CreateTaskform()

        if form.validate_on_submit():
            task.todo = form.task.data
            task.description = form.description.data
            db.session.commit()
            flash("Your task has been Updated!")
            return redirect(url_for("account", task_id=task.id))
        elif request.method == "GET":
            form.task.data = task.todo
            form.description.data = task.description
    return render_template("update_task.html", title="Update task", form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    i.save(picture_path)

    return picture_fn

@app.route("/update-account", methods=["GET", "POST"])
def update_account():

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template("update_account.html", title="Update Account", form=form, image_file=image_file)

@app.route("/delete-task/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    if current_user.is_authenticated:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("account", task_id=task.id))
    
@app.route("/complete/<int:id>", methods=["POST"])
def toggle_complete(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.completed = data.get("completed", False)
    db.session.commit()
    return jsonify({"succes": True, "completed": task.completed}, 201)

