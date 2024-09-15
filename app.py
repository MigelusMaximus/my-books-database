from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    cover_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # New field for categories
    tags = db.Column(db.String(250), nullable=True)  # Add a tags field (comma-separated)
    status = db.Column(db.String(50), nullable=False, default='to read')  # Status: "to read", "reading", "read"
    pages = db.Column(db.Integer, nullable=True)  # Total pages
    pages_read = db.Column(db.Integer, nullable=True, default=0)  # Pages read so far



# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():

    # Get the search query and filters from request.args
    search_query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    
    
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



    books = query.all()  # Fetch the filtered books
    return render_template('index.html', books=books, search_query=search_query, status_filter=status_filter)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
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
def edit_book(id):
    book = Book.query.get_or_404(id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.cover_url = request.form['cover_url']
        book.category = request.form['category']
        book.tags = request.form['tags']  # Make sure tags are updated
        book.status = request.form['status']  # Handle reading status
        book.pages = request.form['pages']    # Handle total pages
        book.pages_read = request.form['pages_read']  # Handle pages read
        
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit_book.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)
