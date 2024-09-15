from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management with Flask-Login
db = SQLAlchemy(app)

# Initialize Flask-Login and Bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if user is not authenticated
bcrypt = Bcrypt(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # True for admin users

# Load the user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    cover_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(250), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='to read')
    pages = db.Column(db.Integer, nullable=True)
    pages_read = db.Column(db.Integer, nullable=True, default=0)
    review = db.Column(db.Text, nullable=True)  # New field for your review
    summary = db.Column(db.Text, nullable=True)  # New field for a book summary

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Get the search query, filters, and sorting from request.args
    search_query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    sort_by = request.args.get('sort_by', 'title')  # Default sorting by title

    # Base query to get all books
    query = Book.query

    # Apply search filter if a query exists
    if search_query:
        query = query.filter(Book.title.contains(search_query) |
                             Book.description.contains(search_query) |
                             Book.tags.contains(search_query))

    # Apply reading status filter if selected
    if status_filter:
        query = query.filter_by(status=status_filter)

    # Sorting logic
    if sort_by == 'title':
        query = query.order_by(Book.title.asc())
    elif sort_by == 'category':
        query = query.order_by(Book.category.asc())
    elif sort_by == 'status':
        query = query.order_by(Book.status.asc())
    elif sort_by == 'progress':
        query = query.order_by((Book.pages_read / Book.pages).desc())  # Sort by progress percentage

    books = query.all()  # Fetch the filtered and sorted books
    return render_template('index.html', books=books, search_query=search_query, status_filter=status_filter, sort_by=sort_by)

@app.route('/add', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def add_book():
    if not current_user.is_admin:  # Check if the user is an admin
        return "Access Denied", 403  # Forbidden if not an admin
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cover_url = request.form['cover_url']
        category = request.form['category']  # Get the category from the form
        tags = request.form['tags']  # Ensure tags are retrieved from the form
        status = request.form['status']  # Handle reading status
        pages = request.form['pages']    # Handle total pages
        pages_read = request.form['pages_read']  # Handle pages read

        # Add the book to the database
        new_book = Book(
            title=title, 
            description=description, 
            cover_url=cover_url, 
            category=category, 
            tags=tags,
            status=status,
            pages=pages,
            pages_read=pages_read
        )
        
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add_book.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def edit_book(id):
    book = Book.query.get_or_404(id)
    
    if not current_user.is_admin:  # Check if the user is an admin
        return "Access Denied", 403  # Forbidden if not an admin

    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.cover_url = request.form['cover_url']
        book.category = request.form['category']
        book.tags = request.form['tags']
        book.status = request.form['status']
        book.pages = request.form['pages']
        book.pages_read = request.form['pages_read']
        book.review = request.form['review']  # Update review
        book.summary = request.form['summary']  # Update summary
        
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>')
@login_required  # Ensure the user is logged in
def delete_book(id):
    if not current_user.is_admin:  # Check if the user is an admin
        return "Access Denied", 403  # Forbidden if not an admin

    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

# Route for the book detail page
@app.route('/book/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)

# Registration route to create admin user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create the admin user
        new_user = User(username=username, password=hashed_password, is_admin=True)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('home'))
    
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
