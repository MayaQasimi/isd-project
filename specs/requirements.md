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
