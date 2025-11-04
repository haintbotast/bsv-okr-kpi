#!/usr/bin/env python3
"""Initialize database - create tables and setup SQLite optimizations."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import *  # Import all models


def init_db():
    """Initialize database."""
    print("Creating database tables...")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Enable SQLite optimizations
    conn = engine.raw_connection()
    cursor = conn.cursor()

    print("Enabling SQLite WAL mode...")
    cursor.execute("PRAGMA journal_mode=WAL")

    print("Configuring SQLite optimizations...")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=10000")
    cursor.execute("PRAGMA foreign_keys=ON")

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Database initialized successfully!")
    print("\nNext steps:")
    print("1. Run: python scripts/create_admin.py --email admin@company.com --password YourPassword123!")
    print("2. Start server: uvicorn app.main:app --reload")


if __name__ == "__main__":
    init_db()
