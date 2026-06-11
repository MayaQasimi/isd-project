"""
Unit tests for PIMIS Library Management System.
Run from project root: pytest tests/
"""
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
