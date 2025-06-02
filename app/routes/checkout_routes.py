from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Book, Checkout
from datetime import datetime

bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@bp.route('/borrow/<int:book_id>')
@login_required
def borrow(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available:
        book.available = False
        checkout = Checkout(user_id=current_user.id, book_id=book.id)
        db.session.add(checkout)
        db.session.commit()
    return redirect(url_for('book.index'))

@bp.route('/return/<int:book_id>')
@login_required
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    checkout = Checkout.query.filter_by(user_id=current_user.id, book_id=book.id, return_date=None).first()
    if checkout:
        checkout.return_date = datetime.utcnow()
        book.available = True
        db.session.commit()
    return redirect(url_for('book.index'))

@bp.route('/history')
@login_required
def history():
    checkouts = Checkout.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', checkouts=checkouts)
