from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import date, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pimis-group1-isd-secret-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── MODELS ─────────────────────────────────────────────────────────

class User(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(20),  default='member')  # admin | member


class Book(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    title            = db.Column(db.String(200), nullable=False)
    author           = db.Column(db.String(100), nullable=False)
    isbn             = db.Column(db.String(20),  unique=True)
    genre            = db.Column(db.String(50))
    total_copies     = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)


class Member(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    phone       = db.Column(db.String(20))
    joined_date = db.Column(db.Date, default=date.today)


class Loan(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    book_id     = db.Column(db.Integer, db.ForeignKey('book.id'),   nullable=False)
    member_id   = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrow_date = db.Column(db.Date, default=date.today)
    due_date    = db.Column(db.Date)
    return_date = db.Column(db.Date, nullable=True)
    status      = db.Column(db.String(20), default='active')  # active | returned
    book        = db.relationship('Book',   backref='loans')
    member      = db.relationship('Member', backref='loans')


# ── AUTH DECORATORS ────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── AUTH ROUTES ────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'user_id' in session else url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            session.update({'user_id': user.id, 'username': user.username, 'role': user.role})
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ── DASHBOARD ──────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
        total_books   = Book.query.count(),
        total_members = Member.query.count(),
        active_loans  = Loan.query.filter_by(status='active').count(),
        overdue       = Loan.query.filter(
                            Loan.status == 'active',
                            Loan.due_date < date.today()).count(),
        recent_loans  = Loan.query.order_by(Loan.borrow_date.desc()).limit(5).all()
    )


# ── CATALOG ROUTES ─────────────────────────────────────────────────

@app.route('/books')
@login_required
def books_list():
    q = request.args.get('q', '').strip()
    if q:
        books = Book.query.filter(
            (Book.title.ilike(f'%{q}%')) |
            (Book.author.ilike(f'%{q}%')) |
            (Book.isbn.ilike(f'%{q}%'))
        ).all()
    else:
        books = Book.query.all()
    return render_template('books/list.html', books=books, q=q)


@app.route('/books/add', methods=['GET', 'POST'])
@admin_required
def books_add():
    if request.method == 'POST':
        copies = int(request.form.get('total_copies', 1))
        db.session.add(Book(
            title            = request.form['title'],
            author           = request.form['author'],
            isbn             = request.form.get('isbn', ''),
            genre            = request.form.get('genre', ''),
            total_copies     = copies,
            available_copies = copies,
        ))
        db.session.commit()
        flash('Book added successfully.', 'success')
        return redirect(url_for('books_list'))
    return render_template('books/add.html')


@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def books_edit(id):
    book = db.get_or_404(Book, id)
    if request.method == 'POST':
        book.title        = request.form['title']
        book.author       = request.form['author']
        book.isbn         = request.form.get('isbn', '')
        book.genre        = request.form.get('genre', '')
        book.total_copies = int(request.form.get('total_copies', 1))
        db.session.commit()
        flash('Book updated.', 'success')
        return redirect(url_for('books_list'))
    return render_template('books/edit.html', book=book)


@app.route('/books/delete/<int:id>', methods=['POST'])
@admin_required
def books_delete(id):
    db.session.delete(db.get_or_404(Book, id))
    db.session.commit()
    flash('Book deleted.', 'warning')
    return redirect(url_for('books_list'))


# ── MEMBER ROUTES ──────────────────────────────────────────────────

@app.route('/members')
@admin_required
def members_list():
    return render_template('members/list.html', members=Member.query.all())


@app.route('/members/add', methods=['GET', 'POST'])
@admin_required
def members_add():
    if request.method == 'POST':
        db.session.add(Member(
            name  = request.form['name'],
            email = request.form['email'],
            phone = request.form.get('phone', ''),
        ))
        db.session.commit()
        flash('Member registered.', 'success')
        return redirect(url_for('members_list'))
    return render_template('members/add.html')


# ── LOAN ROUTES ────────────────────────────────────────────────────

@app.route('/loans')
@admin_required
def loans_list():
    loans = Loan.query.filter_by(status='active').order_by(Loan.due_date).all()
    return render_template('loans/list.html', loans=loans, today=date.today())


@app.route('/loans/new', methods=['GET', 'POST'])
@admin_required
def loans_new():
    if request.method == 'POST':
        book = db.get_or_404(Book, int(request.form['book_id']))
        if book.available_copies < 1:
            flash('No copies available for this book.', 'danger')
            return redirect(url_for('loans_new'))
        book.available_copies -= 1
        db.session.add(Loan(
            book_id     = book.id,
            member_id   = int(request.form['member_id']),
            borrow_date = date.today(),
            due_date    = date.today() + timedelta(days=14),
            status      = 'active',
        ))
        db.session.commit()
        flash('Loan issued successfully.', 'success')
        return redirect(url_for('loans_list'))
    return render_template('loans/new.html',
        books   = Book.query.filter(Book.available_copies > 0).all(),
        members = Member.query.all(),
    )


@app.route('/loans/return/<int:id>', methods=['POST'])
@admin_required
def loans_return(id):
    loan = db.get_or_404(Loan, id)
    loan.return_date = date.today()
    loan.status = 'returned'
    loan.book.available_copies += 1
    db.session.commit()
    flash('Book returned successfully.', 'success')
    return redirect(url_for('loans_list'))


# ── HISTORY ────────────────────────────────────────────────────────

@app.route('/history')
@login_required
def history():
    loans = Loan.query.order_by(Loan.borrow_date.desc()).all()
    return render_template('history.html', loans=loans, today=date.today())


# ── DATABASE INITIALISATION ────────────────────────────────────────

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(
                username      = 'admin',
                email         = 'admin@library.com',
                password_hash = generate_password_hash('admin123'),
                role          = 'admin',
            ))
            db.session.commit()
            print('  Seeded default admin  =>  username: admin  |  password: admin123')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
