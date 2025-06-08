from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the full PostgreSQL URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# (Optional) Test connection immediately
# (Optional) Test connection immediately
if __name__ == "__main__":
    from sqlalchemy import text

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ DB connected:", result.fetchone())
    except Exception as e:
        print("❌ DB connection failed:", e)
