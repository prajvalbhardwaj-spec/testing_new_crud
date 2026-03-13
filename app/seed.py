import bcrypt
from sqlalchemy.orm import Session
from app import models


DUMMY_USERS = [
    {"username": "alice", "email": "alice@example.com", "password": "alice1234"},
    {"username": "bob", "email": "bob@example.com", "password": "bob1234"},
    {"username": "charlie", "email": "charlie@example.com", "password": "charlie1234"},
]

DUMMY_BLOGS = [
    {
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python. It uses type hints for validation and generates docs automatically.",
        "author_index": 0,
    },
    {
        "title": "Why PostgreSQL is Great",
        "content": "PostgreSQL is one of the most advanced open-source relational databases. It supports JSON, full-text search, and much more.",
        "author_index": 1,
    },
    {
        "title": "Building a Blog with Python",
        "content": "In this post we walk through building a full-featured blog API using FastAPI, SQLAlchemy, and PostgreSQL — step by step.",
        "author_index": 2,
    },
    {
        "title": "JWT Authentication Explained",
        "content": "JSON Web Tokens (JWT) allow stateless authentication. The server issues a signed token and the client sends it with every request.",
        "author_index": 0,
    },
    {
        "title": "Deploying FastAPI to Render",
        "content": "Render makes deploying Python web services easy. Just connect your GitHub repo, set your environment variables, and you're live.",
        "author_index": 1,
    },
]


def _hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8")[:72],
        bcrypt.gensalt()
    ).decode("utf-8")


def seed(db: Session) -> bool:
    """
    Insert dummy data if tables are empty.
    Returns True if seeded, False if already had data.
    """
    if db.query(models.User).first():
        print("Database already has data, skipping seed.")
        return False

    users = []
    for u in DUMMY_USERS:
        user = models.User(
            username=u["username"],
            email=u["email"],
            hashed_password=_hash(u["password"])
        )
        db.add(user)
        users.append(user)

    db.flush()  # get user IDs without committing

    for b in DUMMY_BLOGS:
        blog = models.Blog(
            title=b["title"],
            content=b["content"],
            author_id=users[b["author_index"]].id
        )
        db.add(blog)

    db.commit()
    print("Database seeded with dummy data.")
    return True
