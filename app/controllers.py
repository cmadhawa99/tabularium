from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from datetime import date
from .database import SessionLocal
from .models import FileRecord, BorrowRecord


class ArchiveController:
    def __init__(self):
        self.db: Session = SessionLocal()

    def add_new_file(self, data):
        try:
            existing = self.db.query(FileRecord).filter(FileRecord.rr_number == data['rr_number']).first()
            if existing:
                return False, f"Error: RR Number '{data['rr_number']}' already exists!"

            new_file = FileRecord(
                rr_number=data['rr_number'],
                serial_number=data.get('serial_number'),
                sector=data.get('sector'),
                subject_number=data.get('subject_number'),
                file_name=data['file_name'],
                file_type=data.get('file_type', 'Normal'),
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                total_pages=data.get('total_pages', 0),
                shelf_number=data.get('shelf_number'),
                deck_number=data.get('deck_number'),
                file_number=data.get('file_number'),
                current_status="Available"
            )

            self.db.add(new_file)
            self.db.commit()
            return True, f"File '{new_file.file_name}' was successfully added!"

        except Exception as e:
            self.db.rollback()
            return False, f"Database Error: {str(e)}"

    def search_files(self, query_text=""):
        """
        Searches for files. If query is empty, returns ALL files sorted by newest.
        """
        query = self.db.query(FileRecord)

        if query_text:
            search = f"%{query_text}%"
            query = query.filter(
                or_(
                    FileRecord.file_name.ilike(search),
                    FileRecord.rr_number.ilike(search),
                    FileRecord.subject_number.ilike(search),
                    FileRecord.sector.ilike(search)
                )
            )

        # Order by newest (using rr_number or serial_number if you prefer)
        results = query.limit(100).all()
        return results

    def borrow_file(self, rr_number, borrower_name, borrowing_date):
        try:
            file_record = self.db.query(FileRecord).filter(FileRecord.rr_number == rr_number).first()

            if not file_record:
                return False, f"Error: RR Number '{rr_number}' does not exist!"

            if file_record.current_status != "Available":
                return False, f"Cannot borrow: File is currently '{file_record.current_status}'"

            borrow_entity = BorrowRecord(
                file_rr_number=rr_number,
                borrower_name=borrower_name,
                borrowed_date=borrowing_date,
                is_returned=False
            )

            file_record.current_status = "Borrowed"

            self.db.add(borrow_entity)
            self.db.commit()
            return True, f"File '{file_record.file_name}' marked as Borrowed."

        except Exception as e:
            self.db.rollback()
            return False, f"Database Error: {str(e)}"

    def return_file(self, rr_number):
        try:
            active_loan = self.db.query(BorrowRecord).filter(
                BorrowRecord.file_rr_number == rr_number,
                BorrowRecord.is_returned == False
            ).first()

            if not active_loan:
                return False, f"No active borrowing record found for '{rr_number}'."

            active_loan.returned_date = date.today()
            active_loan.is_returned = True

            file_record = self.db.query(FileRecord).filter(FileRecord.rr_number == rr_number).first()
            if file_record:
                file_record.current_status = "Available"

            self.db.commit()
            return True, f"File '{rr_number}' was successfully returned!"

        except Exception as e:
            self.db.rollback()
            return False, f"Database Error: {str(e)}"

    def get_dashboard_stats(self):
        total = self.db.query(FileRecord).count()
        borrowed = self.db.query(FileRecord).filter(FileRecord.current_status == "Borrowed").count()
        removed = self.db.query(FileRecord).filter(FileRecord.current_status == "Removed").count()

        return {
            "total": total,
            "borrowed": borrowed,
            "removed": removed
        }

    def get_circulation_history(self, page=1, page_size=50, search_text=""):
        """
        Fetches borrow records with pagination
        Returns record_list and total_count
        """

        try:
            query = self.db.query(BorrowRecord)

            # 1) Apply Search Filter if text exists
            if search_text:
                search_fmt = f"%{search_text}%"
                query = query.filter(
                    or_(
                        BorrowRecord.file_rr_number.ilike(search_fmt),
                        BorrowRecord.borrower_name.ilike(search_fmt)
                    )
                )

            # 2) Calculate the total
            total_records = query.count()

            # 3) Apply Pagination
            offset = (page - 1) * page_size

            records = query \
                .order_by(desc(BorrowRecord.borrowed_date)) \
                .limit(page_size) \
                .offset(offset) \
                .all()

            return records, total_records

        except Exception as e:
            print(f"History Error: {e}")
            return [], 0

    def get_all_borrow_records(self):
        """
        Fetches all borrow records for exporting
        """
        try:
            # Order by most recent first
            return self.db.query(BorrowRecord).order_by(desc(BorrowRecord.borrowed_date)).all()
        except Exception as e:
            print(f"Export Error: {e}")
            return []
