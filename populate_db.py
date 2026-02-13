import random
from faker import Faker
from app.database import SessionLocal, engine, Base
from app.models import FileRecord, BorrowRecord
from datetime import date, timedelta

fake = Faker()


def populate_data(n=50):
    db = SessionLocal()
    print(f"Generating {n} unique records...")

    sectors = ["Land Division", "Accounts", "Administration", "Planning", "Samurdhi"]
    subjects = ["L-01", "L-02", "AC-55", "AD-10", "PL-99"]

    count = 0
    while count < n:
        # 1. Generate a UNIQUE RR Number
        # We keep generating until we find one that doesn't exist in the DB
        while True:
            year = random.randint(2020, 2026)
            num = random.randint(1000, 9999)
            rr_num = f"RR-{year}-{num}"

            # Check DB to ensure uniqueness
            exists = db.query(FileRecord).filter(FileRecord.rr_number == rr_num).first()
            if not exists:
                break  # Found a unique number!

        file_name = f"{fake.catch_phrase()} - {random.randint(2010, 2025)}"
        sector = random.choice(sectors)

        # 2. Create File Record
        new_file = FileRecord(
            rr_number=rr_num,
            serial_number=random.randint(1, 100000),  # Larger range to avoid serial collision
            sector=sector,
            subject_number=random.choice(subjects),
            file_name=file_name,
            file_type=random.choice(["Normal", "Special"]),
            start_date=fake.date_between(start_date='-5y', end_date='today'),
            end_date=fake.date_between(start_date='-1y', end_date='today'),
            total_pages=random.randint(10, 500),
            shelf_number=random.randint(1, 20),
            deck_number=random.randint(1, 5),
            file_number=random.randint(1, 100),
            current_status="Available"
        )

        # 3. Randomly Borrow some files
        if random.random() < 0.2:
            new_file.current_status = "Borrowed"
            db.add(new_file)
            db.commit()  # Commit immediately to save the File so we can link BorrowRecord

            borrow_entry = BorrowRecord(
                file_rr_number=new_file.rr_number,
                borrower_name=fake.name(),
                borrowed_date=date.today() - timedelta(days=random.randint(1, 30)),
                is_returned=False
            )
            db.add(borrow_entry)
            db.commit()
        else:
            db.add(new_file)
            db.commit()

        count += 1
        print(f"Created {count}/{n}: {rr_num}")

    db.close()
    print("Success! Database populated.")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    populate_data(550)