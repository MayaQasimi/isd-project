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
