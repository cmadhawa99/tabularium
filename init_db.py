from app.database import engine, Base
from app import models

def init_db():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(engine)
        print("Success! Tables 'file_records' and 'borrow_records' created in archive_db.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()