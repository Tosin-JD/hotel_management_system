import sqlite3
from models.rooms_model import RoomModel
from models.guests_model import GuestModel
import uuid

from .db import get_db_path 


class ReservationModel:
    def __init__(self):
        self.room = RoomModel()
        self.guest = GuestModel()
        self.connection = sqlite3.connect(get_db_path("hotel_management.db"))
        self.cursor = self.connection.cursor()
        self.create_table()

    def __str__(self):
        return "Reservation"
        
    def create_table(self):
        # SQL command to create the table
        # SQL command to create the table
        create_table_query = '''CREATE TABLE IF NOT EXISTS reservations (
                                id TEXT PRIMARY KEY,
                                guest_id INTEGER,
                                purpose TEXT,
                                amount_paid REAL,
                                amount_in_words TEXT,
                                payment_type TEXT,
                                room_id INTEGER,
                                check_in_date DATE,
                                check_out_date DATE,
                                FOREIGN KEY (guest_id) REFERENCES guests(id),
                                FOREIGN KEY (room_id) REFERENCES rooms(id)
                                );'''

        # Execute the SQL command
        self.cursor.execute(create_table_query)

        # Commit changes
        self.connection.commit()
    
    def insert_reservation(self, guest_id, purpose, amount_paid, amount_in_words, payment_type, room_id, check_in_date, check_out_date):
        # SQL command to insert a new reservation record
        uuid_value = uuid.uuid4()
        id = str(uuid_value)
        insert_query = '''INSERT INTO reservations (id, guest_id, purpose, amount_paid, amount_in_words, payment_type, room_id, check_in_date, check_out_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?);'''
        
        # Data for the new reservation record
        reservation_data = (id, guest_id, purpose, amount_paid, amount_in_words, payment_type, room_id, check_in_date, check_out_date)

        # Execute the SQL command with the reservation data
        self.cursor.execute(insert_query, reservation_data)
        self.connection.commit()
        self.room.reserve(room_id)
        
    def select_all_reservations(self):
        # SQL command to select all reservation records
        select_all_query = '''SELECT * FROM reservations;'''

        # Execute the SQL command to retrieve all reservations
        self.cursor.execute(select_all_query)

        # Fetch all rows from the database
        all_reservations = self.cursor.fetchall()

        return all_reservations
    
    def get_all_reservation_data(self):
        # SQL command to fetch all reservation data along with guest and room information
        query = '''SELECT reservations.id, 
                    guests.FIRSTNAME, guests.LASTNAME,
                    guests.MOBILE, guests.ADDRESS,
                    rooms.room_number, 
                    reservations.purpose, 
                    reservations.amount_paid, reservations.amount_in_words, reservations.payment_type, 
                    reservations.check_in_date, reservations.check_out_date 
                   FROM reservations
                   INNER JOIN guests ON reservations.guest_id=guests.id
                   INNER JOIN rooms ON reservations.room_id=rooms.room_number;
                   '''
        # Execute the query
        self.cursor.execute(query)
        reservations = self.cursor.fetchall()
        return self.output(reservations)

    def output(self, data):
        reservation_data_list = []
        for reservation_info in data:
            reservation_data = {
                "reservation_id": reservation_info[0],
                "guest_name": f"{reservation_info[1]} {reservation_info[2]}",
                "guest_mobile": reservation_info[3],
                "guest_address": reservation_info[4],
                "room_number": reservation_info[5],
                "purpose": reservation_info[6],
                "amount_paid": reservation_info[7],
                "amount_in_words": reservation_info[8],
                "payment_type": reservation_info[9],
                "check_in_date": reservation_info[10],
                "check_out_date": reservation_info[11]
                # Add more fields as needed
            }
            reservation_data_list.append(reservation_data)
        return reservation_data_list
        
    def find_reservations_by_guest(self, guest_mobile):
        # SQL command to select reservation records for a specific guest
        query = '''SELECT reservations.id, 
                                    guests.FIRSTNAME, guests.LASTNAME, guests.MOBILE, guests.MOBILE,
                                    rooms.room_number, 
                                    reservations.purpose, 
                                    reservations.amount_paid, reservations.amount_in_words, reservations.payment_type, 
                                    reservations.check_in_date, reservations.check_out_date 
                                FROM reservations
                                INNER JOIN guests ON reservations.guest_id = guests.id
                                INNER JOIN rooms ON reservations.room_id = rooms.room_number
                                WHERE guests.MOBILE = ?;
                                '''

        # Fetch all results
        guest_mobile = f"%{guest_mobile}%"
        self.cursor.execute(query, (guest_mobile,))
        reservations = self.cursor.fetchall()
        return self.output(reservations)
    
    def find_by_check_in_date(self, check_in_date):
        # SQL command to select reservation records for a specific check-in date
        query = '''SELECT reservations.id, 
                                    guests.FIRSTNAME, guests.LASTNAME, guests.MOBILE, guests.MOBILE,
                                    rooms.room_number, 
                                    reservations.purpose, 
                                    reservations.amount_paid, reservations.amount_in_words, reservations.payment_type, 
                                    reservations.check_in_date, reservations.check_out_date 
                                FROM reservations
                                INNER JOIN guests ON reservations.guest_id = guests.id
                                INNER JOIN rooms ON reservations.room_id = rooms.room_number
                                WHERE check_in_date LIKE ?;'''

        check_in_date = f"%{check_in_date}%"
        self.cursor.execute(query, (check_in_date,))
        reservations = self.cursor.fetchall()
        return self.output(reservations)
        
    def find_by_check_out_date(self, check_out_date):
        # SQL command to select reservation records for a specific check-out date
        query = '''SELECT reservations.id, 
                                    guests.FIRSTNAME, guests.LASTNAME, guests.MOBILE, guests.MOBILE,
                                    rooms.room_number, 
                                    reservations.purpose, 
                                    reservations.amount_paid, reservations.amount_in_words, reservations.payment_type, 
                                    reservations.check_in_date, reservations.check_out_date 
                                FROM reservations
                                INNER JOIN guests ON reservations.guest_id = guests.id
                                INNER JOIN rooms ON reservations.room_id = rooms.room_number
                                WHERE check_out_date LIKE ?;'''
        check_out_date = f"%{check_out_date}%"
        self.cursor.execute(query, (check_out_date,))
        reservations = self.cursor.fetchall()
        return self.output(reservations)
    
    def delete(self, reservation_id):
        query = '''DELETE FROM rooms WHERE id = ?;'''
        with self.connection:
            self.connection.execute(query, (reservation_id,))
    
    def __del__(self):
        """Close the connection when the object is deleted from memory"""
        self.connection.close()
