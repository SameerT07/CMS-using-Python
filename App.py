from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_ckeditor import CKEditor
from flask import request, redirect, url_for
from flask import render_template
from functools import wraps
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from .models import User
from . import db
from .decorators import admin_required
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from flask_uploads import UploadNotAllowed

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from bleach import clean
clean(user_input, tags=['b', 'i', 'u'], attributes={'a': ['href']})



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# Define the User model and database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






    @app.route('/')
def home():
    return 'Welcome to the CMS'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


    from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User model and database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return 'Welcome to the CMS'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))







# Add CKEditor to your app
ckeditor = CKEditor(app)

# Article form
class ArticleForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')

@app.route('/create_article', methods=['GET', 'POST'])
@login_required  # Ensure only authenticated users can create articles
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # Save the article to the database and associate it with the current user
        # Redirect to the article detail page or another appropriate page
    return render_template('article_form.html', form=form)

@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required  # Ensure only authenticated users can edit articles
def edit_article(article_id):
    # Fetch the article from the database based on the article_id
    # Prepopulate the form fields with the article data
    form = ArticleForm()
    if form.validate_on_submit():
        # Update the article in the database
        # Redirect to the article detail page or another appropriate page
    return render_template('article_form.html', form=form)



# Assume you have a User model and an Article model defined in models.py

# Route for deleting articles
@app.route('/delete_article/<int:article_id>', methods=['POST'])
@login_required  # Ensure only authenticated users can delete articles
def delete_article(article_id):
    # Fetch the article from the database based on the article_id
    article = Article.query.get(article_id)

    if not article:
        # Handle the case where the article doesn't exist
        flash('Article not found.', 'danger')
        return redirect(url_for('home'))

    if current_user != article.author and not current_user.is_admin:
        # Check if the current user is the author or an administrator
        flash('You are not authorized to delete this article.', 'danger')
        return redirect(url_for('article_detail', article_id=article_id))

    # If the user is authorized, delete the article
    db.session.delete(article)
    db.session.commit()

    flash('Article deleted successfully.', 'success')
    return redirect(url_for('home'))



# Assume you have a User model and an Article model defined in models.py

# Route for showing article details
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    # Fetch the article from the database based on the article_id
    article = Article.query.get(article_id)

    if not article:
        # Handle the case where the article doesn't exist
        flash('Article not found.', 'danger')
        return redirect(url_for('home'))

    return render_template('article_detail.html', article=article)



# Route for listing articles with pagination and search/filter
@app.route('/articles', methods=['GET'])
def article_list():
    page = request.args.get('page', type=int, default=1)
    search = request.args.get('search', default='', type=str)
    filter_by = request.args.get('filter', default='all', type=str)

    if filter_by == 'author':
        # Filter by author
        articles = Article.query.filter(Article.author.username.contains(search)).paginate(page, per_page=10)
    elif filter_by == 'tag':
        # Implement tag-based filtering
        # You can add a similar query for tags
        pass
    else:
        # No filter, list all articles
        articles = Article.query.filter(Article.title.contains(search)).paginate(page, per_page=10)

    return render_template('article_list.html', articles=articles)

    

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'user':
            return f(*args, **kwargs)
        flash('You must be logged in as a regular user to access this page.', 'danger')
        return redirect(url_for('home'))
    return decorated_function

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Admin dashboard logic here

@app.route('/user/profile')
@login_required
@user_required
def user_profile():
    # User profile logic here

@app.route('/admin/user_management')
@login_required
@admin_required
def user_management():
    # User management logic here




# Admin interface for user role assignment
@app.route('/admin/assign_roles', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_roles():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('new_role')

        user = User.query.get(user_id)

        if not user:
            flash('User not found.', 'danger')
        else:
            user.role = new_role
            db.session.commit()
            flash('User role updated successfully.', 'success')

    # Fetch all users from the database
    users = User.query.all()
    return render_template('assign_roles.html', users=users)



# Define upload sets for images and documents
images = UploadSet('images', IMAGES)
documents = UploadSet('documents', DOCUMENTS)

# Configure the upload directory and allowed extensions
app.config['UPLOADED_IMAGES_DEST'] = 'path_to_upload_directory_for_images'
app.config['UPLOADED_IMAGES_ALLOW'] = set(['jpg', 'jpeg', 'png', 'gif'])
app.config['UPLOADED_DOCUMENTS_DEST'] = 'path_to_upload_directory_for_documents'
app.config['UPLOADED_DOCUMENTS_ALLOW'] = set(['pdf', 'doc', 'docx'])

configure_uploads(app, (images, documents))



@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image = request.files['image']
        document = request.files['document']

        article = Article(title=title, content=content, author=current_user)

        if image:
            try:
                # Save the image to the upload directory
                image_name = images.save(image)
                article.image = image_name
            except UploadNotAllowed:
                flash('Invalid image file format. Allowed formats: jpg, jpeg, png, gif', 'danger')

        if document:
            try:
                # Save the document to the upload directory
                document_name = documents.save(document)
                article.document = document_name
            except UploadNotAllowed:
                flash('Invalid document file format. Allowed formats: pdf, doc, docx', 'danger')

        db.session.add(article)
        db.session.commit()
        flash('Article created successfully.', 'success')
        return redirect(url_for('article_list'))

    return render_template('article_form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)













