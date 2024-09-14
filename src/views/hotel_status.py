import tkinter as tk
from tkinter import BOTH, BOTTOM, HORIZONTAL, NO, RIGHT, VERTICAL, X, Y, messagebox
from tkinter import ttk
from models.rooms_model import RoomModel


class HotelStatusView:
    def __init__(self, root):
        self.root = root
        self.room_model = RoomModel()
        self.total_rooms = tk.StringVar()
        self.reserved_rooms = tk.StringVar()
        self.unreserved_rooms = tk.StringVar()
        self.create_widget()

    def create_widget(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)

        self.root.rowconfigure(0, weight=1)

        self.total_rooms = self.room_model.get_total_rooms()
        self.reserved_rooms = self.room_model.get_num_of_reserved_rooms()
        self.unreserved_rooms = self.room_model.get_num_of_unreserved_rooms()
        
        first_frame = tk.LabelFrame(self.root, text="Total Rooms", 
                                    relief="flat",
                                    bd=4,
                                    bg='#222255',
                                    fg='#eeeeee',
                                    width=100, height=100,
                                    font=("arial", 20))
        second_frame = tk.LabelFrame(self.root, text="Total Reserved Rooms",
                                     bd=4, width=200, font=("arial", 20),
                                     bg='#225522',
                                     fg='#eeeeee',
                                     relief="flat")
        third_frame = tk.LabelFrame(self.root, text="Available Rooms",
                                    relief="flat", 
                                    bd=4, 
                                    bg='#552222',
                                    fg='#eeeeee',
                                    width=200, height=100,
                                    font=("arial", 20))
        fourth_frame = tk.Frame(self.root, width=200, 
                                relief="flat",
                                height=100)

        first_frame.grid(row=0, column=0, sticky="nsew")
        second_frame.grid(row=0, column=1, sticky="nsew")
        third_frame.grid(row=0, column=2, sticky="nsew")
        fourth_frame.grid(row=0, column=3, sticky="nsew")

        self.lbl_total_rooms = tk.Label(first_frame, text=self.total_rooms,
                                 font=("arial", 40, "bold"),
                                 bg='#222255',
                                 fg='#eeeeee', bd=4)
        self.lbl_total_rooms.pack(fill=X)

        self.lbl_reserved_rooms = tk.Label(second_frame, text=self.reserved_rooms,
                                      font=("arial", 40, "bold"),
                                      bg='#225522',
                                      fg='#eeeeee', bd=4)
        self.lbl_reserved_rooms.pack(fill=X)

        self.lbl_unreserved_rooms = tk.Label(third_frame, text=self.unreserved_rooms, 
                                      font=("arial", 40, "bold"), 
                                      bg='#552222',
                                      fg='#eeeeee', bd=4)
        self.lbl_unreserved_rooms.pack(fill=X)
        btn_refresh = tk.Button(fourth_frame, text="Refresh Hotel Status",
                                bg='#222222',
                                fg='#eeeeee',
                                font=("arial", 20),
                                command=self.refresh)
        btn_refresh.pack(fill=BOTH, expand=True)
        self.refresh()

    def refresh(self):
        self.lbl_total_rooms.config(text=self.room_model.get_total_rooms())
        self.lbl_reserved_rooms.config(text=self.room_model.get_num_of_reserved_rooms())
        self.lbl_unreserved_rooms.config(text=self.room_model.get_num_of_unreserved_rooms())
