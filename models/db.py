import os
import sqlite3

def get_db_path(db_name):
    app_data_dir = os.getenv('APPDATA')
    guesthouse_dir = os.path.join(app_data_dir, 'GuestHouse')
    db_path = os.path.join(guesthouse_dir, db_name)

    if not os.path.exists(guesthouse_dir):
        os.makedirs(guesthouse_dir)

    if not os.path.exists(db_path):
        connection = sqlite3.connect(db_path)
        connection.close()
    return db_path