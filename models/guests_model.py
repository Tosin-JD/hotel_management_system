import sqlite3
import uuid

from .db import get_db_path  

class GuestModel:
    def __init__(self):
        self.connection = sqlite3.connect(get_db_path("hotel_management.db"))
        self.create_table()
        self.cursor = self.connection.cursor()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS guests(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            REF_NO TEXT UNIQUE,
            FIRSTNAME TEXT NOT NULL,
            LASTNAME TEXT NOT NULL,
            GENDER TEXT,
            NEXT_OF_KIN_MOBILE TEXT,
            MOBILE TEXT NOT NULL UNIQUE,
            EMAIL TEXT,
            NATIONALITY TEXT,
            ID_TYPE TEXT,
            ID_NO TEXT,
            ADDRESS TEXT);
        '''
        with self.connection:
            self.connection.execute(query)

    def search_guest_by_phone(self, phone_number):
        query = "SELECT * FROM guests WHERE MOBILE = ?"
        with self.connection:
            cursor = self.connection.execute(query, (phone_number,))
            guest = cursor.fetchone()

        return guest

    def add_guest(self, guest_data):
        uuid_value = uuid.uuid4()
        ref_no = str(uuid_value)
        
        guest_data.insert(0, ref_no)
        query = '''
        INSERT INTO guests (REF_NO, FIRSTNAME, LASTNAME, GENDER, NEXT_OF_KIN_MOBILE, MOBILE, EMAIL, NATIONALITY, ID_TYPE, ID_NO, ADDRESS)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        with self.connection:
            self.connection.execute(query, guest_data)

    def get_cursor(self):
        return self.connection.cursor

    def get_guests(self):
        query = '''
        SELECT * FROM guests
        '''
        with self.connection:
            cursor = self.connection.execute(query)
            return cursor.fetchall()
        
    def search_guests(self, search_by, search_term):
        self.cursor.execute(
            f"SELECT * FROM guests WHERE {search_by} LIKE ?",
            ("%" + search_term + "%",),
        )
        return self.cursor.fetchall()

    def update_guest(self, guest_data):
        query = '''
        UPDATE guests
        SET FIRSTNAME=?, LASTNAME=?, GENDER=?, NEXT_OF_KIN_MOBILE=?, MOBILE=?, EMAIL=?, NATIONALITY=?, ID_TYPE=?, ID_NO=?, ADDRESS=?
        WHERE REF_NO=?
        '''
        with self.connection:
            self.connection.execute(query, guest_data)

    def delete(self, ref_no):
        query = '''
        DELETE FROM guests WHERE REF_NO=?
        '''
        with self.connection:
            self.connection.execute(query, (ref_no,))
            self.connection.commit()

    def __del__(self):
        self.connection.close()
