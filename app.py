from flask import Flask, render_template, redirect, flash, url_for, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from requests import session

from models import db, connect_db, Hardware, User
from forms import AddHardwareForm, EditHardwareForm, UserForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "thequickbrownfoxjumpsoverthelazydog"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hardware_lists"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)
db.create_all()


@app.route('/')
def home_page():

    return render_template("homepage.html")


@app.route("/inside_vault", methods=['GET', 'POST'])
def list_hardware():
    """List all hardwares."""
    hardwares = Hardware.query.all()
    return render_template("inside_vault.html", hardwares=hardwares)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        db.session.commit()

        flash('Welcome! Successfully Created Your Account!')
        return redirect('/inside_vault')

    return render_template('/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")

            return redirect('/inside_vault')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!")
    return redirect('/')


@app.route('/read_me')
def read_me():
    return render_template("read_me.html")


@app.route("/vault", methods=["GET", "POST"])
def add_hardware():
    """Add a listing."""

    form = AddHardwareForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_hardware = Hardware(**data)

        db.session.add(new_hardware)
        db.session.commit()
        flash(f"{new_hardware.name} added.")
        return redirect(url_for('list_hardware'))

    else:
        # re-present form for editing
        return render_template("vault.html", form=form)


@app.route("/<int:hardware_id>", methods=["GET", "POST"])
def edit_hardware(hardware_id):
    """Edit hardware."""

    hardware = Hardware.query.get_or_404(hardware_id)
    form = EditHardwareForm(obj=hardware)

    if form.validate_on_submit():
        hardware.notes = form.notes.data
        hardware.available = form.available.data
        hardware.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{hardware.name} updated.")
        return redirect(url_for('list_hardware'))

    else:
        # failed; re-present form for editing
        return render_template("hardware_edit_form.html", form=form, hardware=hardware)


@app.route("/api/hardwares/<int:hardware_id>", methods=['GET'])
def api_get_hardware(hardware_id):
    """Return basic info about the hardware in JSON."""

    hardware = Hardware.query.get_or_404(hardware_id)
    info = {"name": hardware.name, "price": hardware.price}

    return jsonify(info)
