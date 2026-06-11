#!/usr/bin/env python3
"""
build_library_system.py  —  Group 1 PIMIS
Library Management System — ISD Tutorial (Modules 4-6 combined)

Usage:
    python build_library_system.py

This script scaffolds the full project, then run the app with:
    cd app/library-management
    pip install -r requirements.txt
    python app.py
    # Open http://localhost:5000  |  login: admin / admin123
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))


def write(rel_path, content):
    full = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full) if os.path.dirname(full) else BASE, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK  {rel_path}")


print("=" * 60)
print("  PIMIS Group 1 — Library Management System Builder")
print("=" * 60)

# ══════════════════════════════════════════════════════════════
# SPECS
# ══════════════════════════════════════════════════════════════

write("specs/project-brief.md", """\
# Project Brief: Library Management System

**Group:** 1 PIMIS
**Members:** Maya Zeyad Ahmed Qasimi (24523228) · Gerry Rivanda (24523133)
           Eza Herda Herdiana (24523187) · Candra Dedy Setiawan (24523056)
**Course:** Information System Development (ISD)
**Framework:** GSD Core — Discuss → Plan → Execute → Verify → Ship

---

## Problem Statement
A university library relies on manual paper-based record-keeping for book
loans, member registration, and catalog management. This causes errors,
slow lookups, and no visibility into overdue books. The library needs a
simple web-based digital system to replace these manual processes.

## Goals
1. Digitise the book catalog (add, edit, delete, search)
2. Register and track library members
3. Automate borrowing and return workflows
4. Track loan history and highlight overdue books
5. Provide an admin dashboard with live statistics

## Users
| Role   | Description                                     |
|--------|-------------------------------------------------|
| Admin  | Librarian: full access to all features          |
| Member | Student/reader: view catalog and loan history   |

## Scope
**In-scope (v1):** Authentication, book catalog, member management,
borrow/return, loan history, admin dashboard.
**Out-of-scope (v1):** Email notifications, mobile app, fine/fee system,
book reservations.

## Constraints
- Runs on localhost (single machine, no deployment required)
- Tech stack: Python 3.9+ / Flask / SQLite / Jinja2 / Bootstrap 5
- Deliverable within one ISD tutorial session
- No external paid services or cloud databases
""")

write("specs/requirements.md", """\
# Requirements Specification

## Functional Requirements

### FR-01: Authentication
- System provides a login page (username + password)
- Admin role: full access to all routes
- Member role: read-only access (catalog + history)
- Sessions persist until explicit logout
- Default admin seeded on first run (admin / admin123)

### FR-02: Book Catalog
- Admin can add, edit, and delete books
- Fields: title, author, ISBN, genre, total copies, available copies
- All authenticated users can search by title, author, or ISBN
- Availability displayed as a coloured badge

### FR-03: Member Management
- Admin can register new members (name, email, phone)
- Admin views full member list with active-loan count per member

### FR-04: Borrowing & Returning
- Admin issues a loan by selecting book + member
- Due date defaults to borrow date + 14 days
- Admin processes returns; available copies auto-incremented
- Overdue loans highlighted in red in the active-loans view

### FR-05: Loan History
- All authenticated users can view full loan history (descending)
- Columns: book, member, borrow date, due date, return date, status

### FR-06: Admin Dashboard
- Stats cards: total books, total members, active loans, overdue count
- Table: 5 most recent loans

## Non-Functional Requirements
- NFR-01: Pages load in < 2 seconds on localhost
- NFR-02: Passwords stored as Werkzeug hashes (never plaintext)
- NFR-03: All non-public routes protected by decorators
- NFR-04: Python 3.9+ compatibility

## Acceptance Criteria
- End-to-end flow succeeds: add book → register member → issue loan → return book
- Member user cannot reach /members, /loans/new, or /books/add
- Default admin created automatically on first run
- All pytest unit tests pass
""")

write("specs/architecture.md", """\
# Architecture Document

## Overview
Single-tier Flask monolith. Suitable for tutorial scope; can scale by
swapping SQLite for PostgreSQL and splitting routes into Flask Blueprints.

## Tech Stack
| Layer       | Technology              | Notes                    |
|-------------|-------------------------|--------------------------|
| Language    | Python 3.9+             |                          |
| Framework   | Flask 3.0.0             | WSGI micro-framework     |
| ORM         | Flask-SQLAlchemy 3.1.1  | SQLAlchemy 2.x backend   |
| Database    | SQLite                  | File: library.db         |
| Templates   | Jinja2                  | Bundled with Flask       |
| CSS         | Bootstrap 5.3 (CDN)     | No build toolchain       |
| Auth        | Flask sessions          | Cookie-based, server-side|
| Passwords   | Werkzeug                | Bundled with Flask       |

## Directory Structure
```
app/library-management/
├── app.py               # Entry point, models, auth decorators, all routes
├── requirements.txt     # pip dependencies
├── library.db           # Auto-created SQLite file on first run
├── templates/
│   ├── base.html        # Bootstrap navbar + flash messages
│   ├── login.html
│   ├── dashboard.html
│   ├── history.html
│   ├── books/           # list.html  add.html  edit.html
│   ├── members/         # list.html  add.html
│   └── loans/           # list.html  new.html
└── static/
    └── style.css
specs/                   # All specification documents
tests/
    test_app.py          # pytest unit tests
    requirements.txt     # test dependencies
```

## Data Model (ERD summary)
```
User(id PK, username UNIQUE, email UNIQUE, password_hash, role)
Book(id PK, title, author, isbn UNIQUE, genre, total_copies, available_copies)
Member(id PK, name, email UNIQUE, phone, joined_date)
Loan(id PK, book_id FK→Book, member_id FK→Member,
     borrow_date, due_date, return_date NULL, status)
```

## Request Lifecycle
```
Browser ──► Flask route decorator
            ├─ @login_required  (redirect to /login if not authenticated)
            └─ @admin_required  (flash error + redirect if role != admin)
                    │
                    ▼
            SQLAlchemy ORM  ──►  SQLite (library.db)
                    │
                    ▼
            Jinja2 render_template  ──►  HTML response
```

## Security Measures
- `@login_required` on all authenticated routes
- `@admin_required` on all mutating/admin routes
- `generate_password_hash` / `check_password_hash` via Werkzeug
- Flask `SECRET_KEY` signs session cookies
- No raw SQL; all queries via SQLAlchemy ORM
""")

write("specs/decisions.md", """\
# Architecture & Design Decisions

## Decision Log

| ID     | Decision                              | Rationale                                      | Trade-off                              |
|--------|---------------------------------------|------------------------------------------------|----------------------------------------|
| DEC-01 | Single app.py (no blueprints)         | Lower complexity for tutorial audience         | Less separation of concerns at scale   |
| DEC-02 | SQLite as database                    | Zero-config, Python built-in, file-based       | Not suitable for concurrent production |
| DEC-03 | Flask sessions (not Flask-Login)      | Fewer dependencies, simpler mental model       | No remember-me or token auth           |
| DEC-04 | Bootstrap 5 via CDN                   | No npm/webpack build toolchain needed          | Requires internet connection           |
| DEC-05 | Modules 4-6 combined in one AI turn   | Token efficiency; scope was unambiguous        | Less iterative spec refinement         |
| DEC-06 | Git Worktree per feature branch       | Enables true parallel development              | Requires merge discipline              |

## Team Git Worktree Assignments
| Branch           | Member            | Feature                            |
|------------------|-------------------|------------------------------------|
| feature/auth     | Maya              | Authentication & session management|
| feature/catalog  | Gerry             | Book catalog CRUD & search         |
| feature/members  | Eza               | Member registration & listing      |
| feature/loans    | Candra Dedy       | Borrow/return, history, dashboard  |

## Upgrade Path (post-tutorial)
1. Swap `SQLALCHEMY_DATABASE_URI` to a PostgreSQL URI
2. Refactor routes into Flask Blueprints (one per feature)
3. Add Flask-Migrate for schema migrations
4. Add Flask-Mail for overdue notifications
5. Add pagination to catalog and history views
""")

# ══════════════════════════════════════════════════════════════
# FLASK APPLICATION
# ══════════════════════════════════════════════════════════════

write("app/library-management/requirements.txt", """\
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
""")

write("app/library-management/app.py", """\
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
""")

# ── TEMPLATES ──────────────────────────────────────────────────────

write("app/library-management/templates/base.html", """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Library{% endblock %} — PIMIS Library</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
  <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand fw-bold" href="{{ url_for('dashboard') }}">
      <i class="bi bi-book-half"></i> PIMIS Library
    </a>
    {% if session.user_id %}
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="{{ url_for('dashboard') }}"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('books_list') }}"><i class="bi bi-journals"></i> Catalog</a></li>
        {% if session.role == 'admin' %}
        <li class="nav-item"><a class="nav-link" href="{{ url_for('members_list') }}"><i class="bi bi-people"></i> Members</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('loans_list') }}"><i class="bi bi-arrow-left-right"></i> Loans</a></li>
        {% endif %}
        <li class="nav-item"><a class="nav-link" href="{{ url_for('history') }}"><i class="bi bi-clock-history"></i> History</a></li>
        <li class="nav-item"><a class="nav-link text-warning" href="{{ url_for('logout') }}"><i class="bi bi-box-arrow-right"></i> {{ session.username }}</a></li>
      </ul>
    </div>
    {% endif %}
  </div>
</nav>

<div class="container mt-4">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for cat, msg in messages %}
      <div class="alert alert-{{ cat }} alert-dismissible fade show" role="alert">
        {{ msg }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    {% endfor %}
  {% endwith %}

  {% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

write("app/library-management/templates/login.html", """\
{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-header bg-dark text-white">
        <h5 class="mb-0"><i class="bi bi-lock-fill"></i> Library Login</h5>
      </div>
      <div class="card-body">
        <form method="POST">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input name="username" class="form-control" required autofocus>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-dark w-100">
            <i class="bi bi-box-arrow-in-right"></i> Login
          </button>
        </form>
      </div>
      <div class="card-footer text-muted small text-center">
        Default admin: <strong>admin</strong> / <strong>admin123</strong>
      </div>
    </div>
  </div>
</div>
{% endblock %}
""")

write("app/library-management/templates/dashboard.html", """\
{% extends 'base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-speedometer2"></i> Dashboard</h2>

<div class="row g-3 mb-4">
  <div class="col-6 col-md-3">
    <div class="card text-white bg-primary h-100">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ total_books }}</div>
        <div>Total Books</div>
      </div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card text-white bg-success h-100">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ total_members }}</div>
        <div>Members</div>
      </div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card text-white bg-warning h-100">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ active_loans }}</div>
        <div>Active Loans</div>
      </div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card text-white bg-danger h-100">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ overdue }}</div>
        <div>Overdue</div>
      </div>
    </div>
  </div>
</div>

<h5>Recent Loans</h5>
<div class="table-responsive">
  <table class="table table-striped table-hover align-middle">
    <thead class="table-dark">
      <tr><th>Book</th><th>Member</th><th>Borrowed</th><th>Due</th><th>Status</th></tr>
    </thead>
    <tbody>
      {% for loan in recent_loans %}
      <tr>
        <td>{{ loan.book.title }}</td>
        <td>{{ loan.member.name }}</td>
        <td>{{ loan.borrow_date }}</td>
        <td>{{ loan.due_date }}</td>
        <td>
          <span class="badge bg-{{ 'success' if loan.status == 'returned' else 'warning' }}">
            {{ loan.status }}
          </span>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="5" class="text-muted text-center">No loans yet.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
""")

write("app/library-management/templates/books/list.html", """\
{% extends 'base.html' %}
{% block title %}Book Catalog{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2><i class="bi bi-journals"></i> Book Catalog</h2>
  {% if session.role == 'admin' %}
  <a href="{{ url_for('books_add') }}" class="btn btn-dark">
    <i class="bi bi-plus-lg"></i> Add Book
  </a>
  {% endif %}
</div>

<form class="d-flex mb-3" method="GET">
  <input name="q" value="{{ q }}" class="form-control me-2" placeholder="Search by title, author, or ISBN...">
  <button class="btn btn-outline-secondary" type="submit">Search</button>
  {% if q %}<a href="{{ url_for('books_list') }}" class="btn btn-outline-danger ms-1">Clear</a>{% endif %}
</form>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-dark">
      <tr>
        <th>Title</th><th>Author</th><th>ISBN</th><th>Genre</th><th>Available</th>
        {% if session.role == 'admin' %}<th>Actions</th>{% endif %}
      </tr>
    </thead>
    <tbody>
      {% for book in books %}
      <tr>
        <td>{{ book.title }}</td>
        <td>{{ book.author }}</td>
        <td class="text-muted small">{{ book.isbn }}</td>
        <td class="text-muted small">{{ book.genre }}</td>
        <td>
          <span class="badge bg-{{ 'success' if book.available_copies > 0 else 'danger' }}">
            {{ book.available_copies }} / {{ book.total_copies }}
          </span>
        </td>
        {% if session.role == 'admin' %}
        <td>
          <a href="{{ url_for('books_edit', id=book.id) }}" class="btn btn-sm btn-outline-primary">Edit</a>
          <form method="POST" action="{{ url_for('books_delete', id=book.id) }}" class="d-inline"
                onsubmit="return confirm('Delete this book?')">
            <button class="btn btn-sm btn-outline-danger">Delete</button>
          </form>
        </td>
        {% endif %}
      </tr>
      {% else %}
      <tr><td colspan="6" class="text-muted text-center">No books found.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
""")

write("app/library-management/templates/books/add.html", """\
{% extends 'base.html' %}
{% block title %}Add Book{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-book-half"></i> Add New Book</h2>
<div class="card shadow-sm">
  <div class="card-body">
    <form method="POST">
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Title <span class="text-danger">*</span></label>
          <input name="title" class="form-control" required>
        </div>
        <div class="col-md-6">
          <label class="form-label">Author <span class="text-danger">*</span></label>
          <input name="author" class="form-control" required>
        </div>
        <div class="col-md-4">
          <label class="form-label">ISBN</label>
          <input name="isbn" class="form-control">
        </div>
        <div class="col-md-4">
          <label class="form-label">Genre</label>
          <input name="genre" class="form-control">
        </div>
        <div class="col-md-4">
          <label class="form-label">Total Copies</label>
          <input name="total_copies" type="number" class="form-control" value="1" min="1">
        </div>
      </div>
      <div class="mt-3">
        <button class="btn btn-dark"><i class="bi bi-save"></i> Add Book</button>
        <a href="{{ url_for('books_list') }}" class="btn btn-secondary ms-2">Cancel</a>
      </div>
    </form>
  </div>
</div>
{% endblock %}
""")

write("app/library-management/templates/books/edit.html", """\
{% extends 'base.html' %}
{% block title %}Edit Book{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-pencil-square"></i> Edit Book</h2>
<div class="card shadow-sm">
  <div class="card-body">
    <form method="POST">
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Title <span class="text-danger">*</span></label>
          <input name="title" class="form-control" value="{{ book.title }}" required>
        </div>
        <div class="col-md-6">
          <label class="form-label">Author <span class="text-danger">*</span></label>
          <input name="author" class="form-control" value="{{ book.author }}" required>
        </div>
        <div class="col-md-4">
          <label class="form-label">ISBN</label>
          <input name="isbn" class="form-control" value="{{ book.isbn }}">
        </div>
        <div class="col-md-4">
          <label class="form-label">Genre</label>
          <input name="genre" class="form-control" value="{{ book.genre }}">
        </div>
        <div class="col-md-4">
          <label class="form-label">Total Copies</label>
          <input name="total_copies" type="number" class="form-control" value="{{ book.total_copies }}" min="1">
        </div>
      </div>
      <div class="mt-3">
        <button class="btn btn-dark"><i class="bi bi-save"></i> Update Book</button>
        <a href="{{ url_for('books_list') }}" class="btn btn-secondary ms-2">Cancel</a>
      </div>
    </form>
  </div>
</div>
{% endblock %}
""")

write("app/library-management/templates/members/list.html", """\
{% extends 'base.html' %}
{% block title %}Members{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2><i class="bi bi-people-fill"></i> Members</h2>
  <a href="{{ url_for('members_add') }}" class="btn btn-dark">
    <i class="bi bi-person-plus-fill"></i> Register Member
  </a>
</div>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-dark">
      <tr><th>#</th><th>Name</th><th>Email</th><th>Phone</th><th>Joined</th><th>Active Loans</th></tr>
    </thead>
    <tbody>
      {% for m in members %}
      <tr>
        <td class="text-muted">{{ loop.index }}</td>
        <td>{{ m.name }}</td>
        <td>{{ m.email }}</td>
        <td>{{ m.phone or '—' }}</td>
        <td>{{ m.joined_date }}</td>
        <td>
          <span class="badge bg-secondary">
            {{ m.loans | selectattr('status', 'equalto', 'active') | list | length }}
          </span>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="6" class="text-muted text-center">No members registered.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
""")

write("app/library-management/templates/members/add.html", """\
{% extends 'base.html' %}
{% block title %}Register Member{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-person-plus-fill"></i> Register New Member</h2>
<div class="card shadow-sm">
  <div class="card-body">
    <form method="POST">
      <div class="mb-3">
        <label class="form-label">Full Name <span class="text-danger">*</span></label>
        <input name="name" class="form-control" required autofocus>
      </div>
      <div class="mb-3">
        <label class="form-label">Email <span class="text-danger">*</span></label>
        <input type="email" name="email" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Phone</label>
        <input name="phone" class="form-control" placeholder="Optional">
      </div>
      <button class="btn btn-dark"><i class="bi bi-save"></i> Register</button>
      <a href="{{ url_for('members_list') }}" class="btn btn-secondary ms-2">Cancel</a>
    </form>
  </div>
</div>
{% endblock %}
""")

write("app/library-management/templates/loans/list.html", """\
{% extends 'base.html' %}
{% block title %}Active Loans{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2><i class="bi bi-arrow-left-right"></i> Active Loans</h2>
  <a href="{{ url_for('loans_new') }}" class="btn btn-dark">
    <i class="bi bi-plus-lg"></i> New Loan
  </a>
</div>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-dark">
      <tr><th>Book</th><th>Member</th><th>Borrowed</th><th>Due</th><th>Status</th><th>Action</th></tr>
    </thead>
    <tbody>
      {% for loan in loans %}
      <tr class="{{ 'table-danger' if loan.due_date < today else '' }}">
        <td>{{ loan.book.title }}</td>
        <td>{{ loan.member.name }}</td>
        <td>{{ loan.borrow_date }}</td>
        <td>{{ loan.due_date }}</td>
        <td>
          <span class="badge bg-{{ 'danger' if loan.due_date < today else 'warning' }}">
            {{ 'Overdue' if loan.due_date < today else 'Active' }}
          </span>
        </td>
        <td>
          <form method="POST" action="{{ url_for('loans_return', id=loan.id) }}" class="d-inline"
                onsubmit="return confirm('Mark this book as returned?')">
            <button class="btn btn-sm btn-success"><i class="bi bi-check-lg"></i> Return</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="6" class="text-muted text-center">No active loans.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
""")

write("app/library-management/templates/loans/new.html", """\
{% extends 'base.html' %}
{% block title %}New Loan{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-book-half"></i> Issue New Loan</h2>
<div class="card shadow-sm">
  <div class="card-body">
    <form method="POST">
      <div class="mb-3">
        <label class="form-label">Book <span class="text-danger">*</span></label>
        <select name="book_id" class="form-select" required>
          <option value="">— Select a book —</option>
          {% for book in books %}
          <option value="{{ book.id }}">
            {{ book.title }} — {{ book.author }}
            ({{ book.available_copies }} available)
          </option>
          {% endfor %}
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Member <span class="text-danger">*</span></label>
        <select name="member_id" class="form-select" required>
          <option value="">— Select a member —</option>
          {% for member in members %}
          <option value="{{ member.id }}">{{ member.name }} ({{ member.email }})</option>
          {% endfor %}
        </select>
      </div>
      <p class="text-muted small"><i class="bi bi-info-circle"></i> Due date will be automatically set to 14 days from today.</p>
      <button class="btn btn-dark"><i class="bi bi-save"></i> Issue Loan</button>
      <a href="{{ url_for('loans_list') }}" class="btn btn-secondary ms-2">Cancel</a>
    </form>
  </div>
</div>
{% endblock %}
""")

write("app/library-management/templates/history.html", """\
{% extends 'base.html' %}
{% block title %}Loan History{% endblock %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-clock-history"></i> Loan History</h2>
<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-dark">
      <tr><th>Book</th><th>Member</th><th>Borrowed</th><th>Due</th><th>Returned</th><th>Status</th></tr>
    </thead>
    <tbody>
      {% for loan in loans %}
      <tr>
        <td>{{ loan.book.title }}</td>
        <td>{{ loan.member.name }}</td>
        <td>{{ loan.borrow_date }}</td>
        <td>{{ loan.due_date }}</td>
        <td>{{ loan.return_date if loan.return_date else '—' }}</td>
        <td>
          {% if loan.status == 'returned' %}
            <span class="badge bg-success">Returned</span>
          {% elif loan.due_date < today %}
            <span class="badge bg-danger">Overdue</span>
          {% else %}
            <span class="badge bg-warning">Active</span>
          {% endif %}
        </td>
      </tr>
      {% else %}
      <tr><td colspan="6" class="text-muted text-center">No loan history yet.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
""")

write("app/library-management/static/style.css", """\
/* PIMIS Library Management System — custom styles */
body        { padding-bottom: 60px; background-color: #f8f9fa; }
.navbar     { box-shadow: 0 2px 8px rgba(0,0,0,.25); }
.card       { border-radius: 12px; }
.table      { background: white; }
""")

# ══════════════════════════════════════════════════════════════
# TESTS
# ══════════════════════════════════════════════════════════════

write("tests/requirements.txt", """\
pytest==7.4.3
""")

write("tests/test_app.py", """\
\"\"\"
Unit tests for PIMIS Library Management System.
Run from project root: pytest tests/
\"\"\"
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'library-management'))

import pytest
from app import app, db, User, Book, Member, Loan
from werkzeug.security import generate_password_hash
from datetime import date, timedelta


# ── FIXTURES ───────────────────────────────────────────────────────

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            admin = User(
                username='admin', email='admin@test.com',
                password_hash=generate_password_hash('admin123'), role='admin')
            member_user = User(
                username='member', email='member@test.com',
                password_hash=generate_password_hash('member123'), role='member')
            db.session.add_all([admin, member_user])
            db.session.commit()
        yield client


def do_login(client, username='admin', password='admin123'):
    return client.post('/login',
        data={'username': username, 'password': password},
        follow_redirects=True)


# ── AUTH TESTS ─────────────────────────────────────────────────────

class TestAuth:
    def test_login_page_loads(self, client):
        r = client.get('/login')
        assert r.status_code == 200
        assert b'Login' in r.data

    def test_login_success_admin(self, client):
        r = do_login(client)
        assert b'Dashboard' in r.data

    def test_login_wrong_password(self, client):
        r = client.post('/login',
            data={'username': 'admin', 'password': 'wrong'},
            follow_redirects=True)
        assert b'Invalid' in r.data

    def test_logout(self, client):
        do_login(client)
        r = client.get('/logout', follow_redirects=True)
        assert b'Login' in r.data

    def test_unauthenticated_redirects(self, client):
        for path in ['/dashboard', '/books', '/members', '/history']:
            r = client.get(path, follow_redirects=True)
            assert b'Login' in r.data


# ── BOOK TESTS ─────────────────────────────────────────────────────

class TestBooks:
    def test_books_list_loads(self, client):
        do_login(client)
        r = client.get('/books')
        assert r.status_code == 200

    def test_add_book(self, client):
        do_login(client)
        r = client.post('/books/add', data={
            'title': 'Clean Code', 'author': 'Robert Martin',
            'isbn': '978-0132350884', 'genre': 'Programming', 'total_copies': '2'
        }, follow_redirects=True)
        assert r.status_code == 200
        with app.app_context():
            assert Book.query.filter_by(title='Clean Code').first() is not None

    def test_member_cannot_add_book(self, client):
        do_login(client, 'member', 'member123')
        r = client.get('/books/add', follow_redirects=True)
        assert b'Admin access required' in r.data

    def test_book_search(self, client):
        do_login(client)
        client.post('/books/add', data={
            'title': 'The Pragmatic Programmer', 'author': 'Hunt',
            'isbn': '9780135957059', 'genre': 'Tech', 'total_copies': '1'
        }, follow_redirects=True)
        r = client.get('/books?q=Pragmatic')
        assert b'Pragmatic' in r.data


# ── MEMBER TESTS ───────────────────────────────────────────────────

class TestMembers:
    def test_members_list_loads(self, client):
        do_login(client)
        r = client.get('/members')
        assert r.status_code == 200

    def test_add_member(self, client):
        do_login(client)
        r = client.post('/members/add', data={
            'name': 'Alice Smith', 'email': 'alice@test.com', 'phone': '555-1234'
        }, follow_redirects=True)
        assert r.status_code == 200
        with app.app_context():
            assert Member.query.filter_by(email='alice@test.com').first() is not None

    def test_member_cannot_access_members_list(self, client):
        do_login(client, 'member', 'member123')
        r = client.get('/members', follow_redirects=True)
        assert b'Admin access required' in r.data


# ── LOAN TESTS ─────────────────────────────────────────────────────

class TestLoans:
    def _seed(self):
        with app.app_context():
            book   = Book(title='Test Book', author='Author A', total_copies=2, available_copies=2)
            member = Member(name='Bob Jones', email='bob@test.com')
            db.session.add_all([book, member])
            db.session.commit()
            return book.id, member.id

    def test_issue_loan(self, client):
        do_login(client)
        book_id, member_id = self._seed()
        r = client.post('/loans/new',
            data={'book_id': str(book_id), 'member_id': str(member_id)},
            follow_redirects=True)
        assert r.status_code == 200
        with app.app_context():
            loan = Loan.query.first()
            assert loan is not None
            assert loan.status == 'active'
            assert Book.query.get(book_id).available_copies == 1

    def test_return_loan(self, client):
        do_login(client)
        book_id, member_id = self._seed()
        client.post('/loans/new',
            data={'book_id': str(book_id), 'member_id': str(member_id)},
            follow_redirects=True)
        with app.app_context():
            loan_id = Loan.query.first().id
        r = client.post(f'/loans/return/{loan_id}', follow_redirects=True)
        assert r.status_code == 200
        with app.app_context():
            loan = db.session.get(Loan, loan_id)
            assert loan.status == 'returned'
            assert loan.return_date == date.today()
            assert Book.query.get(book_id).available_copies == 2

    def test_no_copies_available(self, client):
        do_login(client)
        with app.app_context():
            book   = Book(title='Rare Book', author='X', total_copies=1, available_copies=0)
            member = Member(name='Carol', email='carol@test.com')
            db.session.add_all([book, member])
            db.session.commit()
            bid, mid = book.id, member.id
        r = client.post('/loans/new',
            data={'book_id': str(bid), 'member_id': str(mid)},
            follow_redirects=True)
        assert b'No copies available' in r.data


# ── DASHBOARD TESTS ────────────────────────────────────────────────

class TestDashboard:
    def test_dashboard_loads_with_stats(self, client):
        do_login(client)
        r = client.get('/dashboard')
        assert r.status_code == 200
        assert b'Dashboard' in r.data
        assert b'Total Books' in r.data
""")

# ══════════════════════════════════════════════════════════════
# README
# ══════════════════════════════════════════════════════════════

write("README.md", """\
# PIMIS Library Management System

**Group 1 PIMIS** — ISD Tutorial (GSD Core framework)

## Members
| Name                   | NIM      | Feature Branch    |
|------------------------|----------|-------------------|
| Maya Zeyad Ahmed Qasimi| 24523228 | feature/auth      |
| Gerry Rivanda          | 24523133 | feature/catalog   |
| Eza Herda Herdiana     | 24523187 | feature/members   |
| Candra Dedy Setiawan   | 24523056 | feature/loans     |

## Quick Start

```bash
cd app/library-management
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
# Login: admin / admin123
```

## Run Tests

```bash
pip install pytest
pytest tests/
```

## Features
- Authentication (role-based: Admin / Member)
- Book Catalog with search
- Member Registration
- Borrow & Return with availability tracking
- Loan History
- Admin Dashboard with stats

## Tech Stack
Python 3.9+ · Flask 3.0 · SQLite · Jinja2 · Bootstrap 5
""")

# ══════════════════════════════════════════════════════════════
# GIT WORKTREE SETUP SCRIPT (helper)
# ══════════════════════════════════════════════════════════════

write("scripts/setup_worktrees.sh", """\
#!/bin/bash
# Run from the repository root after: git init && git add . && git commit -m "init"
git worktree add ../lms-auth    feature/auth
git worktree add ../lms-catalog feature/catalog
git worktree add ../lms-members feature/members
git worktree add ../lms-loans   feature/loans
echo "Worktrees created:"
git worktree list
""")

print()
print("=" * 60)
print("  All files created successfully!")
print("=" * 60)
print()
print("  Next steps:")
print("  1. cd app/library-management")
print("  2. pip install -r requirements.txt")
print("  3. python app.py")
print("  4. Open http://localhost:5000")
print("     Login: admin / admin123")
print()
print("  Run tests:")
print("  1. pip install pytest")
print("  2. pytest tests/ -v")
print()
