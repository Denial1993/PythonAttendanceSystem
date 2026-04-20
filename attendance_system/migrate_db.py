import sys
import os

# Add the directory containing the app module to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from sqlalchemy import text

# Import all models so Base.metadata can create them
import app.models

def migrate():
    with engine.begin() as conn:
        try:
            # Add hire_date to users
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS hire_date DATE;"))
            print("Successfully added hire_date to users.")
        except Exception as e:
            print(f"Error altering users table (might already exist): {e}")

    # Create new tables (Holidays, LeaveBalances)
    Base.metadata.create_all(bind=engine)
    print("Base.metadata.create_all completed.")

if __name__ == "__main__":
    migrate()
