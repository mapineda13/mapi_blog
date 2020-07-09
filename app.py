from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse

from database import db
from forms import SignupForm, PostForm, LoginForm
from models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mapi_Keyword'
# Configuracion de DB
USER_DB = 'postgres'
PASS_DB = 'an63m0n13'
URL_DB = 'localhost'
NAME_DB = 'mapi_blog'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# inicializar objeto app
db.init_app(app)

# configurar flask migrate
migrate = Migrate()
migrate.init_app(app, db)
# redirigir el usuario a la pagina de login para cuando el usuario quiera ver una vista protegida
login_manager = LoginManager(app)
login_manager.login_view = "login"


@app.route("/")
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)


@app.route("/p/<string:slug>")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)


# es mejor tener un solo formulario para ambos propositos insertar y actualizar
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>", methods=['GET', 'POST'])
@login_required  # solo usuarios autenticados acceden a esta funcionalidad
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
