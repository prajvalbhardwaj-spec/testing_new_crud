"""
Standalone seed script — run manually with: python seed.py
"""
from app.database import engine, Base, SessionLocal
from app import seed as seeder

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
    db = SessionLocal()
    try:
        seeder.seed(db)
    finally:
        db.close()
    print("Database seeded successfully!")
