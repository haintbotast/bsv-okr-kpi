#!/usr/bin/env python
"""Initialize default KPI categories in the database."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.crud.system import system_settings


# Default categories requested by user
DEFAULT_CATEGORIES = [
    "Network",
    "System",
    "Operation",
    "Software",
    "BA (Business Analyst)",
    "Tester",
    "Implementation",
    "Administrative",
    "Manager/Deputy Manager",
]


def init_categories():
    """Initialize default KPI categories."""
    db = SessionLocal()
    try:
        # Check if categories already exist
        existing_categories = system_settings.get_categories(db)

        if existing_categories:
            print(f"✅ Categories already initialized: {len(existing_categories)} categories found")
            print(f"   Categories: {', '.join(existing_categories)}")
            return

        # Initialize with default categories
        system_settings.set_categories(db, DEFAULT_CATEGORIES)
        print(f"✅ Initialized {len(DEFAULT_CATEGORIES)} default KPI categories:")
        for i, category in enumerate(DEFAULT_CATEGORIES, 1):
            print(f"   {i}. {category}")

    except Exception as e:
        print(f"❌ Error initializing categories: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Initializing default KPI categories...")
    init_categories()
    print("✅ Done!")
