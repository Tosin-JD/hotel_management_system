import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models.rooms_model import RoomModel

class RoomController:
    def __init__(self, view, root):
        self.root = root
        self.view = view
        self.model = RoomModel()
        self.create_widgets()

    def create_widgets(self):
        ################ LABEL FRAME ###################
        lblFrameLeft = tk.LabelFrame(self.root, 
                                     relief="flat", text="ADD ROOMS",
                                     font=("arial", 12, "bold"))
        lblFrameLeft.grid(row=1, column=0, sticky='nsew')
        lblFrameLeft.columnconfigure(0, weight=1)
        lblFrameLeft.columnconfigure(1, weight=1)

        lblFrameRight = ttk.LabelFrame(self.root, border=2, relief="flat", 
                                       text="ROOMS DETAILS")
        lblFrameRight.grid(row=1, column=1, sticky="nsew")

        # Room Details
        self.label_room_number = tk.Label(lblFrameLeft, text="Room Number:",
                                          font=("arial", 12, "bold"))
        self.label_room_category = tk.Label(lblFrameLeft, text="Room Category:",
                                            font=("arial", 12, "bold"))
        self.label_room_price = tk.Label(lblFrameLeft, text="Price:",
                                         font=("arial", 12, "bold"))



        self.entry_room_number = ttk.Entry(lblFrameLeft)
        room_category_var = tk.StringVar()
        self.combo_room_category = ttk.Combobox(lblFrameLeft, textvariable=room_category_var)
        self.combo_room_category["values"] = ("Double Executive Suite",
                                              "Double Deluxe Suite",
                                              "Single Executive Suite",
                                              "Single Deluxe Suite",
                                              "Men's Hall",
                                              "Women's Hall",
                                              "Others"
                                              )
        self.combo_room_category.current()
        self.entry_room_price = ttk.Entry(lblFrameLeft)


        self.label_room_number.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.label_room_category.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label_room_price.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.entry_room_number.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combo_room_category.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.entry_room_price.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        self.button_add = tk.Button(lblFrameLeft, text="Add Room", 
                                    bg='#222255',
                                    fg='#eeeeee',
                                    command=self.add_room)
        self.button_add.grid(row=4, column=1, columnspan=1, 
                             padx=5, pady=5, sticky="ew")

        self.button_update = tk.Button(lblFrameLeft, text="Update Room", 
                                       bg='#225522',
                                       fg='#eeeeee',
                                       command=self.update)
        self.button_update.grid(row=5, column=1, columnspan=1, 
                                padx=5, pady=5, sticky="ew")

        self.button_delete = tk.Button(lblFrameLeft, text="Delete Room", 
                                       bg='#552222',
                                       fg='#eeeeee',
                                       command=self.delete)
        
        # self.button_delete.grid(row=6, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        self.button_reset = tk.Button(lblFrameLeft, text="Reset", 
                                      bg='#222222',
                                      fg='#eeeeee',
                                      command=self.clear_entries)
        self.button_reset.grid(row=7, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        labelframe_reserve_room = tk.LabelFrame(lblFrameLeft, text="Reserve Room", padx=5, pady=5)
        labelframe_reserve_room.grid(row=8, column=0, columnspan=2, sticky="nsew")

        self.button_reserve_or_unreserve_room = tk.Button(labelframe_reserve_room,
                                                           bg='#225522',
                                                           fg='#eeeeee',
                                                           text="Reserve/Unreserve Room")
        self.button_reserve_or_unreserve_room.pack()

        number_of_rows = lblFrameLeft.grid_size()[1]
        for row_index in range(number_of_rows):
            lblFrameLeft.rowconfigure(row_index, weight=1)

    def populate_entry_fields(self, room_number, room_category, room_price):
        self.entry_room_number.delete(0, tk.END)
        self.entry_room_number.insert(0, room_number)
        
        self.combo_room_category.delete(0, tk.END)
        self.combo_room_category.insert(0, room_category)
        
        self.entry_room_price.delete(0, tk.END)
        self.entry_room_price.insert(0, room_price)

    def add_room(self):
        room_number = self.entry_room_number.get()
        room_category = self.combo_room_category.get()
        room_price = self.entry_room_price.get()

        if room_number and room_category and room_price:
            try:
                self.model.insert_room(room_number, room_category, room_price)
            except sqlite3.IntegrityError:
                # Handle the unique constraint violation here
                messagebox.showerror("Error", "{}Room with the given room number already exists.")
            except Exception as e:
                messagebox.showerror("Error", f"{e}\nContact the developer!")
            else:
                self.view.refresh()
                messagebox.showinfo("Room Added", "The room has been added successfully.")
                self.view.refresh()
                self.clear_entries()
        else:
            messagebox.showwarning("Error", "Please fill in all the required fields.")

    def reserve_or_unreserve(self, room_number):
        selected_item = self.view.tree.selection()
        if selected_item:
            values = self.view.tree.item(selected_item)["values"]
            if values:
                room_number, reserved_status = values[1][5:], values[4]
                if reserved_status == "Yes":
                    self.button_reserve_or_unreserve_room.config(text="Unreserve")
                    self.model.reserve_or_unreserve_room(room_number, 0)
                    messagebox.showinfo("Unreserved", f"Room {room_number} has been successfully unreserved.")
                    self.view.refresh()
                else:
                    self.button_reserve_or_unreserve_room.config(text="Reserve")
                    self.model.reserve_or_unreserve_room(room_number, 1)
                    messagebox.showinfo("Reserved", f"Room{room_number} has been successfully reserved.")
                    self.view.refresh()
        else:
            messagebox.showwarning("Warning", "Select a room in the table.")

    def update(self):
        room_number = self.entry_room_number.get()
        room_category = self.combo_room_category.get()
        room_price = self.entry_room_price.get()

        if room_number and room_category and room_price:
            try:
                # Get the selected row index
                index = self.view.tree.focus()

                # Get the room data from the selected row
                room_data = self.view.tree.item(index)['values']
                
                # Update the room data
                room_data[1] = room_number
                room_data[2] = room_category
                room_data[3] = room_price
                
                # Update the room in the database
                self.model.update(*room_data[:4])

                # Refresh the room list
                self.view.refresh()

                # Display a success message
                messagebox.showinfo("Room Updated", "The room has been updated successfully.")
            except Exception as e:
                # Handle the unique constraint violation here
                messagebox.showerror("Error", f"{e}\ Contact the Developer.")
        else:
            messagebox.showwarning("Error", "Please fill in all the required fields.")


    def delete(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            selected_room = self.view.tree.item(selected_item, "values")
            response = messagebox.askyesno("Confirmation", 
                                           f"""Do you want to delete {selected_room[1]}?""")
            if response:
                self.model.delete_by_room_number(selected_room[1][5:])
                messagebox.showinfo("Delete Successful", f"{selected_room[1]} has been deleted.")
                self.clear_entries()
                self.view.refresh()
            else:
                # Perform the action for 'No' choice 
                messagebox.showinfo("Canceled", "Deletion operation canceled.")             
        else:
            messagebox.showwarning("Error", "Please select a room to delete.")

    def clear_entries(self):
        self.entry_room_number.delete(0, tk.END)
        self.combo_room_category.delete(0, tk.END)
        self.entry_room_price.delete(0, tk.END)

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Create an instance of the ReservationController class
    room_controller = RoomController(root)

    # Start the tkinter event loop
    root.mainloop()
