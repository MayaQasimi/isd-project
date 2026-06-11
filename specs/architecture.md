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
