from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
# Initialize the app
db.init_app(app)

all_books = []

# Create schema
with app.app_context():
    db.create_all()


# Create table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    books = result.scalars()
    return render_template('index.html', books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        rating = request.form.get('rating')

        book = {
            'title': name,
            'author': author,
            'rating': rating
        }

        try:
        # Create record in table
            new_book = Book(title=book['title'], author=book['author'], rating=book['rating'])
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()  # Rollback the changes in case of an error
            return f'Error: {str(e)}'

        # all_books.append(new_book)
        # return render_template('index.html', books=all_books, length=len(all_books))

    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        # UPDATE RECORD
        book_id = request.form['id']
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)

    return render_template('edit.html', book=book_selected)

@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)