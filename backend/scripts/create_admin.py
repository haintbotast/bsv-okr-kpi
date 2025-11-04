#!/usr/bin/env python3
"""Create admin user from command line."""

import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate, UserRole


def create_admin(email: str, password: str, fullname: str):
    """Create admin user."""
    db = SessionLocal()

    try:
        # Check if user already exists
        existing_user = user_crud.get_by_email(db, email=email)
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            return False

        # Create admin user
        user_data = UserCreate(
            email=email,
            username=email.split("@")[0],  # Use email prefix as username
            password=password,
            full_name=fullname,
            role=UserRole.ADMIN,
            department="IT",
            position="System Administrator",
        )

        user = user_crud.create(db, obj_in=user_data)

        print(f"✅ Admin user created successfully!")
        print(f"\nDetails:")
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        print(f"  Full Name: {user.full_name}")
        print(f"  Role: {user.role}")
        print(f"\nYou can now login with:")
        print(f"  Email: {user.email}")
        print(f"  Password: (the password you provided)")

        return True

    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        return False
    finally:
        db.close()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create admin user")
    parser.add_argument("--email", required=True, help="Admin email address")
    parser.add_argument("--password", required=True, help="Admin password (min 8 chars)")
    parser.add_argument("--fullname", required=True, help="Admin full name")

    args = parser.parse_args()

    # Validate password
    if len(args.password) < 8:
        print("❌ Password must be at least 8 characters long!")
        sys.exit(1)

    # Create admin
    success = create_admin(args.email, args.password, args.fullname)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
