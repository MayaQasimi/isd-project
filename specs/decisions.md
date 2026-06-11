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
