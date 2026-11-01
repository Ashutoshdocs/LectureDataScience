"""
Database layer (SQLAlchemy Core).

Works with MySQL on the Azure VM (DATABASE_URL=mysql+pymysql://...) and
falls back to a local SQLite file for quick laptop testing.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, MetaData,
                        String, Table, Text, UniqueConstraint, create_engine)
from sqlalchemy.dialects import mysql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'bookverse.db')}")

# The two demo accounts that can log in (username -> password).
DEMO_USERS = {
    "alice": os.getenv("ALICE_PASSWORD", "alice123"),
    "bob": os.getenv("BOB_PASSWORD", "bob123"),
}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=1800, future=True)
metadata = MetaData()

LongText = Text().with_variant(mysql.LONGTEXT(), "mysql")

users = Table(
    "users", metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=False),
    Column("username", String(50), unique=True, nullable=False),
    Column("full_name", String(100)),
    Column("city", String(60)),
    Column("email", String(120)),
    Column("password_hash", String(255)),  # only demo users have one
)

books = Table(
    "books", metadata,
    Column("book_id", Integer, primary_key=True, autoincrement=False),
    Column("title", String(200), nullable=False),
    Column("author", String(120)),
    Column("genre", String(40), index=True),
    Column("year", Integer),
    Column("pages", Integer),
)

ratings = Table(
    "ratings", metadata,
    Column("rating_id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.user_id"), nullable=False, index=True),
    Column("book_id", Integer, ForeignKey("books.book_id"), nullable=False, index=True),
    Column("rating", Float, nullable=False),
    Column("rated_at", DateTime),
    UniqueConstraint("user_id", "book_id", name="uq_user_book"),
)

friendships = Table(
    "friendships", metadata,
    Column("user_a", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("user_b", Integer, ForeignKey("users.user_id"), primary_key=True),
)

# What each logged-in user is currently looking at (powers the "live view").
user_activity = Table(
    "user_activity", metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True, autoincrement=False),
    Column("view", String(60)),
    Column("title", String(200)),
    Column("payload", LongText),
    Column("updated_at", DateTime),   # last time the screen changed
    Column("last_seen", DateTime),    # heartbeat (online indicator)
)

# Shared activity feed ("bob liked The Silent Signal").
activity_log = Table(
    "activity_log", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.user_id"), index=True),
    Column("action", String(255)),
    Column("created_at", DateTime),
)
