from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Book

bp = Blueprint('book', __name__)

@bp.route('/', methods=['GET'])
def index():
    query = Book.query

    title = request.args.get('title')
    author = request.args.get('author')
    language = request.args.get('language')
    year = request.args.get('year')

    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if language:
        query = query.filter(Book.language.ilike(f'%{language}%'))
    if year:
        query = query.filter(Book.year == year)

    books = query.all()
    return render_template('books.html', books=books)

@bp.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            year=request.form['year'],
            language=request.form['language']
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('book.index'))
    return render_template('add_book.html')

@bp.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = request.form['year']
        book.language = request.form['language']
        db.session.commit()
        return redirect(url_for('book.index'))
    return render_template('edit_book.html', book=book)

@bp.route('/book/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book.index'))
