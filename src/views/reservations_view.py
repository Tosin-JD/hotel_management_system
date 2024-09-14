import os
import tkinter as tk
from tkinter import ttk
from tkinter import Label, FLAT, messagebox
from models.reservations_model import ReservationModel
from controllers.reservations_controller import ReservationController
from print_to_file.print_to_file import PrintRecord, PrintReceipt


from datetime import datetime

class ReservationView:
    def __init__(self, root):
        self.root = root
        self.model = ReservationModel()
        self.controller = ReservationController(root, self, self.model)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=5)
        # Create the Treeview widget to display reservations
        ################ Title ##################
        lbl_title = Label(self.root, text="RESERVATIONS", 
                          font=("arial",18,"bold"), 
                          background="#222222", foreground="#eeeeee", bd=4, relief=FLAT)
        lbl_title.grid(row=0, column=0, columnspan=2, sticky='ew')

        lblFrameRight = tk.LabelFrame(self.root, bd=2, relief="flat", 
                                      text="RESERVATION DETAILS", 
                                      font=("arial", 12, "bold"))
        lblFrameRight.grid(row=1, column=1, sticky="nsew")
        lblFrameRight.columnconfigure(0, weight=1)
        lblFrameRight.rowconfigure(1, weight=1)

        frame1 = tk.Frame(lblFrameRight)    
        search_frame = tk.Frame(lblFrameRight, pady=5)    
        search_frame.grid(row=0, column=0, sticky='ew')
        lbl_search = tk.Label(search_frame, text="Search By", font=("arial", 12, "bold"), bg="#ff0000")
        self.combo_search_by = ttk.Combobox(search_frame, width=25, font=("arial", 12, "bold"), state="readonly")
        self.combo_search_by["value"] = ("GUEST PHONE NUMBER", "CHECK IN DATE", "CHECK OUT DATE")
        self.combo_search_by.current(0)
        self.entry_search = tk.Entry(search_frame, width=15, font=("arial", 14, "bold"))
        btn_search = tk.Button(search_frame, text="Search", bg="#222255", 
                               fg="#eeeeee", font=("arial", 12, "bold"),
                               command=self.search)
        btn_show_all = tk.Button(search_frame, text="Show All", bg="#222222", fg="#eeeeee", font=("arial", 12, "bold"), command=self.refresh)

        lbl_search.grid(row=0, column=0, padx=5, sticky='nsew')
        self.combo_search_by.grid(row=0, column=1, padx=5, sticky='nsew')
        self.entry_search.grid(row=0, column=2, pady=5, padx=5, sticky='nsew')
        btn_search.grid(row=0, column=3, padx=5, sticky='nsew')
        btn_show_all.grid(row=0, column=4, padx=5, sticky='nsew')

        frame1.grid(row=1, column=0, sticky='nsew')

        self.tree = ttk.Treeview(frame1)
        self.tree["columns"] = (
            "reservation_id", "Guest Name", "Address", 
            "Phone Number", "Allocated Suite/ Hall Number", "Purpose", 
            "Amount Paid", "Amount Paid In Words", "Payment Type",
            "Check In Date", "Check Out Date"
        )

        self.tree.heading("#0", text="ID")
        self.tree.column("#0", width=0, stretch="no")
        for column in self.tree["columns"]:
            column_heading = column.replace("_", " ")
            self.tree.heading(column, text=column_heading.title(), anchor='w')
            self.tree.column(column, width=100)
        
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Create a Scrollbar
        scrollbar_y = tk.Scrollbar(frame1, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=4, sticky='ns')

        # Link the Scrollbar to the Listbox
        self.tree.config(yscrollcommand=scrollbar_y.set)

        # # horizontal scrollbar
        scrollbar_x = tk.Scrollbar(frame1, orient=tk.HORIZONTAL, command=self.tree.xview)

        # Horizontal scroll bar for the Tree Table
        self.tree.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.grid(row=4, column=0, sticky='ew')

        frame1.columnconfigure(0, weight=1)
        frame1.rowconfigure(0, weight=1)

        frame2 = tk.Frame(lblFrameRight, padx=5)    
        # Displaying the frame2 in row 0 and column 1
        frame2.grid(row=5, column=0)
        self.button_refresh = tk.Button(frame2, text="Refresh Reservation List",
                                        bg='#222255',
                                        fg='#eeeeee',
                                        width=25, height=3,
                                        command=self.refresh)
        # Button for printing Receipt
        self.button_receipt = tk.Button(frame2, text="Print Receipt", 
                                        width=15, height=3,
                                        bg='#225522',
                                        fg='#eeeeee',
                                        command=self.print_receipt)
        self.button_all_to_csv = tk.Button(frame2, text="Print all to CSV", 
                                        width=15, height=3, 
                                        bg='#552255',
                                        fg='#eeeeee',
                                        command=self.print_all_to_csv)
        self.button_refresh.pack(side="left")
        self.button_receipt.pack(side="left")
        self.button_all_to_csv.pack(side="left")

        # Load reservations data and populate the Treeview
        self.refresh()

        num_columns = lblFrameRight.grid_size()[0]

        # Set the weight of all rows to 1
        lblFrameRight.rowconfigure(1, weight=1)

        # Set the weight of all columns to 1
        for col_index in range(num_columns):
            lblFrameRight.columnconfigure(col_index, weight=1)

    def refresh(self):
        # Get all reservations from the database
        all_reservations = self.model.get_all_reservation_data()
        
        # Clear existing data in the Treeview
        self.tree.delete(*self.tree.get_children())

        # Populate the Treeview with the reservations data
        self.fill_table(all_reservations)


    def fill_table(self, data):
        for reservation in data:
            reservation_id = reservation["reservation_id"]
            guest_name = reservation["guest_name"]
            guest_mobile = reservation["guest_mobile"]
            guest_address = reservation["guest_address"]
            room_number = reservation["room_number"]
            purpose = reservation["purpose"]
            amount_paid = reservation["amount_paid"]
            amount_in_words = reservation["amount_in_words"]
            payment_type = reservation["payment_type"]
            check_in_date = reservation["check_in_date"]
            check_out_date = reservation["check_out_date"]
            
            self.tree.insert("", "end", text=reservation_id, values=(reservation_id, 
                                                                     guest_name, 
                                                                     guest_address, 
                                                                     guest_mobile, 
                                                                     room_number, 
                                                                     purpose, 
                                                                     amount_paid, 
                                                                     amount_in_words, 
                                                                     payment_type, 
                                                                     check_in_date, 
                                                                     check_out_date))
            
    def search(self):
        self.tree.delete(*self.tree.get_children())
        search_item = self.entry_search.get()
        search_by = self.combo_search_by.get()
        if search_item:
            if search_by == "GUEST PHONE NUMBER":
                rows = self.model.find_reservations_by_guest(guest_mobile=search_item)
            elif search_by == "CHECK IN DATE":
                rows = self.model.find_by_check_in_date(check_in_date = search_item)
            elif search_by == "CHECK OUT DATE":
                rows = self.model.find_by_check_out_date(check_out_date = search_item)
            else:
                rows = None
            if rows:
                self.fill_table(rows)
            else:
                messagebox.showerror("Not Found!", "No reservation match!")
        else:
            messagebox.showwarning("No Entry", "Enter a Value to search!")

    def fetch_data(self):
        rows = self.model.get_guests()
        if len(rows) != 0:
            self.tree.delete(*self.tree.get_children())
            for i in rows:
                self.tree.insert("", tk.END, values=i)

    def search_data(self):
        rows_fetch = self.model.search_guests(
            str(self.search_var.get()), str(self.txt_search.get())
        )
        if len(rows_fetch) != 0:
            self.tree.delete(*self.tree.get_children())
            for i in rows_fetch:
                self.tree.insert("", tk.END, values=i)

    def print_receipt(self):
        selected_row = self.tree.selection()
        if selected_row:
            selected_item = self.tree.item(selected_row[0])
            row_data = selected_item.get("values")
            if row_data and isinstance(row_data, (list, tuple)):
                receipt = PrintReceipt(row_data)
                receipt.print_receipt()
                messagebox.showinfo("Success", "Receipt generated successfully.")
            else:
                messagebox.showwarning("Warning", "Invalid reservation data.")
        else:
            messagebox.showwarning("Warning", "Select a reservation to print.")

    def print_all_to_csv(self):
        # Get the main Documents directory for the operating system
        documents_directory = os.path.expanduser("~/Documents")

        # Create a folder called _guest_house in the Documents directory
        os.makedirs(documents_directory + "/_guest_house/reports", exist_ok=True)

        # Get the current date and time
        now = datetime.today()
        current_time_and_date = now.strftime("%Y%m%d_%H%M%S")

        # Create a PrintToClass object for the reservations_`current_time_and_date`.csv file
        print_to_class = PrintRecord(documents_directory + "/_guest_house/reservations_" + current_time_and_date + ".csv")

        # Write the row data to the CSV file
        for row in self.tree.get_children():
            row_data = self.tree.item(row)["values"]
            print_to_class.write_row(row_data)
        messagebox.showinfo("Successfully generated", "Record has been successfully generated")
