import sqlite3
import datetime

from .db import get_db_path 


class RoomModel:
    def __init__(self):
        self.connection = sqlite3.connect(get_db_path("hotel_management.db"))
        self.cursor = self.connection.cursor()
        self.create_table()
        # self.auto_unreserve()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY,
                    room_number INTEGER UNIQUE NOT NULL,
                    room_category INTEGER,
                    room_price INTEGER,
                    is_reserved INTEGER
                );'''
        with self.connection:
            self.connection.execute(query)
        
    def insert_room(self, room_number, room_category, room_price):
        is_reserved = False
        insert_query = '''INSERT INTO rooms (room_number, room_category, room_price, is_reserved)
                VALUES (?, ?, ?, ?);'''
        # Data for the new deposit record
        room_data = (room_number, room_category, room_price, is_reserved)

        try:
            # Execute the SQL command with the room data
            self.cursor.execute(insert_query, room_data)
            # Commit changes
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            # If there's a unique constraint violation, raise your guestom exception
            raise Exception("Room with the given room number already exists.") from e
        
    def get_rooms_by_number(self, room_number):
        query = "SELECT * FROM rooms WHERE room_number LIKE ?"
        with self.connection:
            cursor = self.connection.execute(query, (f"%{room_number}%",))
            rows = cursor.fetchall()
        return rows
    
    def select_all_rooms(self):
        query = '''SELECT * FROM rooms;'''
        with self.connection:
            cursor = self.connection.execute(query)
            return cursor.fetchall()
        
    def fetch_room_by_id(self, room_id):
        query = '''SELECT * FROM rooms WHERE id = ?;'''
        with self.connection:
            cursor = self.connection.execute(query, (room_id,))
            return cursor.fetchone()
        
    def get_unreserved(self):
        query = '''SELECT * FROM rooms WHERE is_reserved = 0;'''
        with self.connection:
            cursor = self.connection.execute(query)
            reserved_rooms = cursor.fetchall()
            return reserved_rooms
        
    def get_reserved(self):
        query = '''SELECT * FROM rooms WHERE is_reserved = 1;'''
        with self.connection:
            cursor = self.connection.execute(query)
            reserved_rooms = cursor.fetchall()
            return reserved_rooms
        
    def update(self, room_id, room_number, room_category, room_price):
        is_reserved = False
        query = '''UPDATE rooms 
                SET room_number = ?, room_category = ?, room_price = ?, is_reserved = ?
                WHERE id = ?;'''
        with self.connection:
            self.connection.execute(query, (room_number, room_category, room_price, is_reserved, room_id))
        
    def reserve(self, room_id):
        query = "UPDATE rooms SET is_reserved = 1 WHERE room_number = ?"
        with self.connection:
            self.connection.execute(query, (room_id,))
            self.connection.commit()
            # self.connection.close()

    def reserve_or_unreserve_room(self, room_number, is_reserved):
        """Reserves or unreserves a room.

        Args:
            room_number (int): The room number to reserve or unreserve.
            is_reserved (bool): Whether to reserve (True) or unreserve (False) the room.
        """
        query = '''UPDATE rooms SET is_reserved = ? WHERE room_number = ?;'''
        with self.connection:
            self.connection.execute(query, (is_reserved, room_number))
            self.connection.commit()

    def fetch_unreserved_rooms(self):
        """ Method for get rooms for reservations to be made """
        query = """ SELECT * FROM  rooms WHERE  is_reserved = 0;"""
        with self.connection:
            cursor = self.connection.execute(query)
            unreserved_rooms = cursor.fetchall()
        if unreserved_rooms:
            return unreserved_rooms
        else:
            raise NoReservedRoomsError

    def auto_unreserve(self):
        """automatically unreserve date once it is today's date"""
        # Get the current date
        today = datetime.date.today()

        # Update all rooms that are reserved for today to be unreserved
        try:
            with self.connection:
                query = '''UPDATE rooms
                        SET is_reserved = 0
                        WHERE is_reserved = 1
                        AND id IN (SELECT room_id FROM reservations WHERE check_out_date = CURRENT_DATE);
                        '''
                self.connection.execute(query)
                self.connection.commit()
        except sqlite3.Error as e:
            pass
        finally:
            pass

    def get_total_rooms(self)->str:
        """Gets the total number of rooms in the database."""
        query = "SELECT COUNT(*) FROM rooms;"
        with self.connection:
            result = self.connection.execute(query)
            number_of_rooms = result.fetchone()[0]
        return str(number_of_rooms)

    def get_num_of_reserved_rooms(self)->str:
        query = "SELECT COUNT(*) FROM rooms WHERE is_reserved = 1;"
        with self.connection:
            result = self.connection.execute(query)
            number_of_rooms = result.fetchone()[0]
        return str(number_of_rooms)

    def get_num_of_unreserved_rooms(self)->str:
        query = "SELECT COUNT(*) FROM rooms WHERE is_reserved = 0;"
        with self.connection:
            result = self.connection.execute(query)
            number_of_rooms = result.fetchone()[0]
        return str(number_of_rooms)

    def delete(self, room_id):
        query = '''DELETE FROM rooms WHERE id = ?;'''
        with self.connection:
            self.connection.execute(query, (room_id,))

    def delete_by_room_number(self, room_number):
        query = '''DELETE FROM rooms WHERE room_number = ?;'''
        with self.connection:
            self.connection.execute(query, (room_number,))
    
    def __del__(self):
        self.connection.close()


class NoReservedRoomsError(Exception):
    def __init__(self, message="No reserved rooms were found."):
        self.message = message
        super().__init__(self.message)