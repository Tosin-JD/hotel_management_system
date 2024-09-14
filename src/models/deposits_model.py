import sqlite3

from .db import get_db_path 


class DepositModel:
    def __init__(self):
        self.connection = sqlite3.connect(get_db_path("hotel_management.db"))
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # SQL command to create the table
        create_table_query = '''CREATE TABLE IF NOT EXISTS deposits (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                guest_id INTEGER,
                                deposits_name TEXT,
                                description TEXT,
                                date_deposited DATE,
                                date_collected DATE,
                                is_collected INTEGER,
                                FOREIGN KEY (guest_id) REFERENCES guests(id)
                                );
                            '''

        # Execute the SQL command
        self.cursor.execute(create_table_query)

        # Commit changes
        self.connection.commit()

    def insert(self, guest_phone_number, deposits_name, description, date_deposited, date_collected):
        is_collected = False
        # SQL command to insert a new deposit record
        insert_query = '''INSERT INTO deposits (guest_id, deposits_name, description, date_deposited, date_collected, is_collected)
                          VALUES (?, ?, ?, ?, ?, ?);'''
        
        guest_id = self.get_guest_by_phone_number(guest_phone_number)
        deposit_data = (guest_id, deposits_name, description, date_deposited, date_collected, is_collected)
        self.cursor.execute(insert_query, deposit_data)
        self.connection.commit()

    def update(self, guest_phone_number, deposits_name, description, date_deposited, date_collected):
        """
        Update an existing deposit record in the deposits table.

        Args:
            guest_phone_number (str): Phone number of the guest associated with the deposit.
            deposits_name (str): New name of the deposit.
            description (str): New description of the deposit.
            date_deposited (str): New date when the deposit was made.
            date_collected (str): New date when the deposit was collected.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        # SQL command to update an existing deposit record
        update_query = '''UPDATE deposits
                        SET deposits_name = ?,
                            description = ?,
                            date_deposited = ?,
                            date_collected = ?
                        WHERE guest_id = ?;
                    '''

        try:
            guest_id = self.get_guest_by_phone_number(guest_phone_number)
            
            # Execute the UPDATE query with the new deposit data
            self.cursor.execute(update_query, (deposits_name, description, date_deposited, date_collected, guest_id))
            
            # Commit changes
            self.connection.commit()
            return True
        except Exception as e:
            print("Error updating deposit:", e)
            self.connection.rollback()
            return False

    def get_guest_by_phone_number(self, guest_phone_number):
        self.cursor.execute('SELECT * FROM guests WHERE MOBILE = ?', (guest_phone_number,))
        guest = self.cursor.fetchone()
        if not guest:
            raise ValueError(f"Guest with Phone Number {guest_phone_number} not found. Please add the guest first.")
        return guest[0]
    
    def mark_deposit_collected(self, deposit_id):
        # SQL command to update the is_collected value
        update_query = '''UPDATE deposits
                        SET is_collected = 1
                        WHERE id = ?;
                    '''
        self.cursor.execute(update_query, (deposit_id,))
        self.connection.commit()
    
    def select_all(self):
        query = '''
            SELECT d.*, c.FIRSTNAME, c.LASTNAME, c.MOBILE
            FROM deposits AS d
            JOIN guests AS c ON d.guest_id = c.id;
        '''
        self.cursor.execute(query)
        all_deposits = self.cursor.fetchall()
        return all_deposits

    def find_deposits_by_guest(self, guest_mobile):
        query = '''
                    SELECT d.*, c.FIRSTNAME, c.LASTNAME, c.MOBILE
                    FROM deposits AS d
                    JOIN guests AS c ON d.guest_id = c.id
                    WHERE c.MOBILE = ?;
                '''
        self.cursor.execute(query, (guest_mobile,))
        guest_deposits = self.cursor.fetchall()
        return guest_deposits

    def find_by_deposit_date(self, deposit_date):
        query = '''
                    SELECT d.*, c.FIRSTNAME, c.LASTNAME, c.MOBILE
                    FROM deposits AS d
                    JOIN guests AS c ON d.guest_id = c.id
                    WHERE d.date_deposited LIKE ?;
                '''
        deposit_date = f"%{deposit_date}%"
        self.cursor.execute(query, (deposit_date,))
        reservation_deposits = self.cursor.fetchall()
        return reservation_deposits
    
    def find_by_collect_date(self, collect_date):
        query = '''
                    SELECT d.*, c.FIRSTNAME, c.LASTNAME, c.MOBILE
                    FROM deposits AS d
                    JOIN guests AS c ON d.guest_id = c.id
                    WHERE d.date_collected LIKE ?;
                '''
        collect_date = f"%{collect_date}%"
        self.cursor.execute(query, (collect_date,))
        reservation_deposits = self.cursor.fetchall()
        return reservation_deposits
    
    def delete(self, deposit_id):
        query = '''DELETE FROM deposits WHERE id = ?;'''
        with self.connection:
            self.connection.execute(query, (deposit_id,))

    def __del__(self):
        """Close the connection when the object is deleted from memory"""
        self.connection.close()
