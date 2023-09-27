import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from os import stat
import sqlite3
from tkinter import*
from PIL import Image, ImageTk #pip install pillow
from tkinter import ttk
import random
from time import strftime
from datetime import datetime
from tkinter import messagebox

# Import the ReservationModel class here
# Make sure you have the ReservationModel class defined properly
from models.reservations_model import ReservationModel
from models.rooms_model import NoReservedRoomsError, RoomModel
from models.guests_model import GuestModel

class ReservationController:
    def __init__(self, root, view, model):
        self.root = root
        self.model = model
        self.view = view
        self.guest_model = GuestModel()
        self.room_model = RoomModel()
        self.create_widgets()

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        # Create labels and entry widgets for data input
        ################ LABEL FRAME ###################
        lblFrameLeft = tk.LabelFrame(self.root, bd=2, relief=FLAT, 
                                     text="RESERVE A ROOM", 
                                     font=("arial", 12, "bold"), padx=2)
        lblFrameLeft.grid(row=1, column=0, sticky='nsew')
        lblFrameLeft.columnconfigure(0, weight=1)
        lblFrameLeft.columnconfigure(1, weight=1)


        self.label_guest_id = tk.Label(lblFrameLeft, text="Guest Phone:", font=("arial", 12, "bold"))
        self.entry_guest_id = tk.Entry(lblFrameLeft)

        self.btn_search_guest = tk.Button(lblFrameLeft, text="Search", command=self.show_popup,
                                          font=("arial", 12, "bold"))

        # Grid layout for widgets
        self.label_guest_id.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.entry_guest_id.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.btn_search_guest.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.btn_search_guest.config(background="green", foreground="white", activebackground="yellow", activeforeground="black")
        
    def clear_entries(self):
        # Clear the input fields after adding, updating, or deleting a reservation
        self.entry_guest_id.delete(0, tk.END)
        self.entry_purpose.delete(0, tk.END)
        self.entry_amount_paid.delete(0, tk.END)
        self.entry_amount_in_words.delete(0, tk.END)
        self.entry_check_in_date.delete(0, tk.END)
        self.entry_check_out_date.delete(0, tk.END)

    def show_popup(self):
        if self.entry_guest_id.get():
            guest = self.guest_model.search_guest_by_phone(self.entry_guest_id.get())
            if guest:
                try:
                    unreserverd_rooms = self.room_model.fetch_unreserved_rooms()
                except NoReservedRoomsError:
                    messagebox.showerror("No reserved rooms!", "All rooms are currently booked!")
                else:
                    popup_window = tk.Toplevel(self.root, takefocus=True)
                    popup_window.title(f"Reserve a room for guest{2} {3}")
                    popup_window.transient(self.root)
                    popup_window.lift(aboveThis=None)
                    popup_window.grab_set()

                    # get the guest id
                    self.guest_id = guest[0]

                    # Arrange the widgets in a grid
                    guest_name = tk.Label(popup_window, text=f"Guest Name: {guest[2]} {guest[3]}",
                                             font=("arial", 14, "bold"),
                                             padx=20, pady=10, fg="#111166")
                    guest_name.grid(row=0, column=0, sticky="w")

                    guest_phone = tk.Label(popup_window, text=f"Guest Phone: {guest[6]}", 
                                              font=("arial", 14, "bold"),
                                              padx=20, pady=10, fg="#111166")
                    guest_phone.grid(row=1, column=0, sticky="w")

                    self.reserve_form(popup_window)

                    selected_room_id = self.combobox_room_id.get() 
            else:
                messagebox.showerror("Not Registered", "Register the Guest.", parent=self.root)
        else:
            messagebox.showwarning("Enter a number", "Enter the guest's phone number.", parent=self.root)

    def submit(self, frame):
        submit_button = tk.Button(frame, text="Submit", command=frame.destroy)
        submit_button.grid(row=2, column=0, pady=5)

    def on_payment_type_selected(self, event):
        selected_payment_type = self.payment_type_combo.get()
        return selected_payment_type

    def add_reservation(self):
        # Get data from the entry fields
        guest_id = self.guest_id
        purpose = self.entry_purpose.get()
        amount_paid_str = self.entry_amount_paid.get()
        amount_in_words = self.entry_amount_in_words.get()
        payment_type = self.payment_type_combo.get()
        room_id = self.combobox_room_id.get()
        check_in_date = self.entry_check_in_date.get()
        check_out_date = self.entry_check_out_date.get()

        # Check if any of the required fields are empty
        if not all([guest_id, purpose, amount_paid_str, amount_in_words, room_id, check_in_date, check_out_date]):
            messagebox.showerror("Incomplete Form", "Please fill all the fields before adding a reservation.", parent=self.root)
            return  # Exit the method early if any required field is empty

        # Validate and handle the amount_paid input
        try:
            amount_paid = float(amount_paid_str.replace(",", ""))
        except Exception:
            # Display an error messagebox when amount_paid is not a valid float
            messagebox.showerror("Invalid Amount Paid", "Amount Paid should be a number.", parent=self.root)
        try:
            self.model.insert_reservation(
                                    guest_id, purpose, 
                                    amount_paid, amount_in_words,
                                    payment_type, 
                                    room_id, check_in_date, 
                                    check_out_date)
            messagebox.showinfo("Successful", "Room successfuly reserved!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", "An error occured kindly contact the developer!", parent=self.root)
        
        self.view.refresh()
        # Clear the input fields
        self.clear_entries()

    def update_reservation(self):
        # Get data from the entry fields
        guest_id = self.entry_guest_id.get()
        purpose = self.entry_purpose.get()
        # replace comma with empty strings and convert it to float
        amount_paid = float((self.entry_amount_paid.get().replace(",", "")))
        amount_in_words = self.entry_amount_in_words.get()
        payment_type = self.payment_type_combo.get()
        room_id = self.entry_room_id.get()
        check_in_date = self.entry_check_in_date.get()
        check_out_date = self.entry_check_out_date.get()
        
        try:
            self.model.update_reservation(
                                    guest_id, purpose, 
                                    amount_paid, amount_in_words, 
                                    room_id, check_in_date, 
                                    check_out_date)
            messagebox.showinfo("Updated Successfully!", "Reservation successfuly updated!", parent=self.root)
        except:
            messagebox.showerror("Error", "An error occured", parent=self.root)

        # Clear the input fields
        self.clear_entries()

    def delete(self):
        # Get data from the entry fields
        guest_id = self.entry_guest_id.get()

        self.model.delete(guest_id)

        # Clear the input fields
        self.clear_entries()

    def reserve_form(self, frame):
        
        self.label_room_id = tk.Label(frame, text="Room Number:",
                                      font=("arial", 12, "bold"))
        
        # self.combobox_room_id = ttk.Combobox(frame, state="readonly", textvariable=self.selected_room_id)
        # self.combobox_room_id['values'] = [tup[1] for tup in self.room_model.fetch_unreserved_rooms()]

        room_data = self.room_model.fetch_unreserved_rooms()
        self.combobox_room_id = ttk.Combobox(frame, state="readonly")
        self.combobox_room_id['values'] = [f"{tup[1]} {tup[2]}" for tup in room_data]

        self.combobox_room_id.bind("<<ComboboxSelected>>", self.on_combobox_select)

        self.label_purpose = tk.Label(frame, text="Purpose:",
                                      font=("arial", 12, "bold"))
        self.entry_purpose = tk.Entry(frame)

        self.label_amount_paid = tk.Label(frame, text="Amount Paid:",
                                          font=("arial", 12, "bold"))
        self.entry_amount_paid = tk.Entry(frame)

        self.label_amount_in_words = tk.Label(frame, text="Amount In Words:",
                                              font=("arial", 12, "bold"))
        self.entry_amount_in_words = tk.Entry(frame)

        self.label_payment_type = tk.Label(frame, text="Select Payment Type:",
                                           font=("arial", 12, "bold"))
        payment_types = ("Cash", "POS", "Transfer", "Cheque")
        self.payment_type_combo = ttk.Combobox(frame, values=payment_types)
        self.payment_type_combo.current(0)
        self.payment_type_combo.bind("<<ComboboxSelected>>", self.on_payment_type_selected)
        
        self.label_check_in_date = tk.Label(frame, text="Check-in Date:",
                                            font=("arial", 12, "bold"))
        self.entry_check_in_date = DateEntry(frame, date_pattern="yyyy-mm-dd")

        self.label_check_out_date = tk.Label(frame, text="Check-out Date:",
                                             font=("arial", 12, "bold"))
        self.entry_check_out_date = DateEntry(frame, date_pattern="yyyy-mm-dd")

        self.label_room_id.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.combobox_room_id.grid(row=2, column=1, padx=10, pady=10)

        self.label_purpose.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_purpose.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.label_amount_paid.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_amount_paid.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.label_amount_in_words.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_amount_in_words.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.label_payment_type.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.payment_type_combo.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        self.label_check_in_date.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.entry_check_in_date.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        self.label_check_out_date.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.entry_check_out_date.grid(row=8, column=1, padx=10, pady=10, sticky="ew")
        
        # Create buttons for CRUD operations
        self.button_add = tk.Button(frame, text="Add Reservation", 
                                    bg='#222255',
                                    fg='#eeeeee',
                                    command=self.add_reservation)
        self.button_update = tk.Button(frame, text="Update Reservation",
                                       bg='#225522',
                                       fg='#eeeeee',
                                       command=self.update_reservation)
        self.button_delete = tk.Button(frame, text="Delete Reservation",
                                       bg='#552222',
                                       fg='#eeeeee',
                                       command=self.delete)

        self.button_add.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        # self.button_update.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        # self.button_delete.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
    def on_combobox_select(self, event):
        selected_value = self.combobox_room_id.get()
        selected_room_id = str(selected_value.split()[0])
        self.combobox_room_id.set(selected_room_id)


if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Create an instance of the ReservationController class
    reservation_controller = ReservationController(root)

    # Start the tkinter event loop
    root.mainloop()
