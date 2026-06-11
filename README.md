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
