# Todo List with User Authentication

A Flask web application with SQLite database, user authentication, and todo management.

## Features

- ✅ User signup and login with password hashing
- ✅ Create todos with persistent storage
- ✅ Mark todos as complete/incomplete
- ✅ Delete todos
- ✅ User-specific todo lists (each user only sees their own)
- ✅ Session-based authentication
- ✅ SQLite database for data persistence

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS
- Werkzeug (password hashing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/drewdavis816/TodoListDB.git
cd TodoListDB
```

2. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python3 main.py
```

5. Open `http://127.0.0.1:5000`

## How to Use

1. Sign up with a username and password
2. Login with your credentials
3. Add todos on your dashboard
4. Mark todos complete/incomplete
5. Delete todos you're done with
6. Logout when finished

## What I Learned

- SQLite database design and SQL queries
- User authentication and password hashing
- Flask-SQLAlchemy ORM
- Session management
- Database relationships (one-to-many)
- Security best practices (password hashing)

## Future Improvements

- Edit todo titles
- Due dates for todos
- Todo categories/tags
- Email notifications
- Dark mode
