# 📚 Bookerino
Web app for sorting my book collection.

Python+Flask+SQLAlchemy

- HTML - Templates
- External styles.css
- External script.js
- Using Bootstrap


## Description
This should be Application priamrly for my own personal use as my book colection grew considerably over the past few years.


## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)




## Features
- 📖 **Add and Edit Books**: Add new books with detailed information such as title, description, category, tags, and more.
- 🔍 **Search and Filter**: Search for books by title, description, or tags, and filter by reading status or category.
- 📊 **Track Reading Progress**: Monitor your reading progress with a visual progress bar.
- 💾 **Upload Book Covers**: Upload custom book cover images or use URLs for book covers.
- ✨ **User-Friendly UI**: Modern, responsive, and mobile-friendly interface with creative hover effects and a dark mode toggle.


## Screenshots
*TO BE ADDED*


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/my-books-database.git
    ```
2. Navigate to the project directory:
    ```bash
    cd my-books-database
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Initialize the database and create tables:
    ```bash
    flask db upgrade
    ```
6. Run the application:
    ```bash
    flask run
    ```



## Usage
- Navigate to the homepage to view all books in your collection.
- Click "Add a New Book" to input book details.
- Use the search bar and filters to find specific books based on categories or tags.
- Click on a book card to view detailed information and personal reviews.
- Only admins can add or edit book entries; general users can only browse the collection.




## Technologies Used
- **Flask**: Backend web framework.
- **Flask-SQLAlchemy**: Database ORM.
- **Flask-Migrate**: Database migrations.
- **Flask-Login**: User authentication.
- **Flask-Bcrypt**: Password hashing.
- **Bootstrap**: Frontend framework for responsive UI.


## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/my-feature`.
5. Open a pull request.



## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---
> Developed with ❤️ by [Migelus Maximus](https://migelusmaximus.github.io/https-migelusmaximus.github.io-/index.html)

