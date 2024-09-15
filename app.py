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

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    books = Book.query.all()  # Fetch all books from the database
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cover_url = request.form['cover_url']
        category = request.form['category']  # Get the category from the form

        # Add the book to the database
        new_book = Book(title=title, description=description, cover_url=cover_url, category=category)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
