from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class FileRecord(Base):
    __tablename__ = 'file_records'

    # --- PRIMARY KEY & IDENTIFIERS ---

    rr_number = Column(String, primary_key=True, index=True, nullable=False)
    serial_number = Column(Integer, unique=True, index=True, nullable=False)

    # --- FILE DETAILS ---

    sector = Column(String, nullable=False)
    subject_number = Column(String)
    file_name = Column(String, nullable=False)
    file_type = Column(String)

    start_date = Column(Date)
    end_date = Column(Date)

    total_pages = Column(Integer)

    # --- LOCATION ---

    shelf_number = Column(Integer)
    deck_number = Column(Integer)
    file_number = Column(Integer)

    # --- STATUS TRACKING ---
    # Status: 'Available', 'Borrowed', 'Removed'
    current_status = Column(String, default="Available")

    # --- REMOVAL DETAILS ---
    to_be_removed_date = Column(Date, nullable=True)
    removed_date = Column(Date, nullable=True)
    is_removed = Column(Boolean, default=False)

    #Relationship to borrowing history
    borrow_history = relationship("BorrowRecord", back_populates="file")

class BorrowRecord(Base):
    __tablename__ = 'borrow_records'

    id = Column(Integer, primary_key=True, index=True)

    # --- FOREIGN KEY CHANGE ---
    file_rr_number = Column(String, ForeignKey('file_records.rr_number'), nullable=False)

     # --- BORROWING DETAILS ---
    borrower_name = Column(String, nullable=False)
    borrowed_date = Column(Date, nullable=False)

    # --- RETURN DETAILS ---
    returned_date = Column(Date, nullable=True)
    is_returned = Column(Boolean, default=False)

    # Link back to parent file
    file = relationship("FileRecord", back_populates="borrow_history")

class User(Base):
    __tablename__ = 'users'

    id =  Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="Viewer")

    # Security Fields
    totp_secret = Column(String, nullable=True) #2FA
    is_active = Column(Boolean, default=True)

