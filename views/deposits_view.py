import os
from os import stat
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk #pip install pillow
from tkinter import ttk
import random
from time import strftime
from datetime import datetime
from tkinter import messagebox
from tkinter.font import Font

from models.deposits_model import DepositModel
from controllers.deposits_controller import DepositController

from print_to_file.print_to_file import PrintReceipt, PrintRecord, PrintDeposits

class DepositView:
    def __init__(self, root):
        self.root = root
        self.model = DepositModel()
        self.controller = DepositController(self, self.root)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        font = ("arial", 12, "bold")
        # Create the Treeview widget to display deposits
        ################ Title ##################
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=5)
        self.root.rowconfigure(1, weight=5)
        lbl_title = tk.Label(self.root, text="DEPOSITS", 
                             font=("arial", 18, "bold"), 
                             bg="#222222", fg="#eeeeee", bd=4,
                             relief="flat")
        lbl_title.grid(row=0, column=0, columnspan=2, sticky='ew')

        ################ LABEL FRAME ###################
        lblFrameLeft = tk.LabelFrame(self.root, bd=2, relief="flat",
                                     text="DEPOSIT A PAYMENT",
                                     font=("arial", 12, "bold"), padx=2)
        lblFrameLeft.grid(row=1, column=0, sticky='nsew')
        lblFrameLeft.columnconfigure(0, weight=1)
        lblFrameLeft.columnconfigure(1, weight=1)

        # controller handling the form
        self.controller.create_widgets(lblFrameLeft)

        lblFrameRight = tk.LabelFrame(self.root, bd=2, relief="flat", 
                                      text="DEPOSIT DETAILS",
                                      font=font, padx=2)
        lblFrameRight.grid(row=1, column=1, sticky="nsew")
        lblFrameRight.columnconfigure(0, weight=1)
        
        frame1 = tk.Frame(lblFrameRight)    
        search_frame = tk.Frame(lblFrameRight, pady=5)    
        search_frame.grid(row=0, column=0, sticky='ew')
        lbl_search = tk.Label(search_frame, text="Search By", font=("arial", 12, "bold"), bg="#ff0000")
        self.combo_search_by = ttk.Combobox(search_frame, width=25, font=("arial", 12, "bold"), state="readonly")
        self.combo_search_by["value"] = ("GUEST PHONE NUMBER", "DEPOSIT DATE", "COLLECT DATE")
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

        self.tree = ttk.Treeview(frame1, columns=("deposit_id", "item_name", "guest_name", 
                                "description", "date_deposited", 
                                "date_collected", "is_collected"),)
        self.tree.grid(row=0, column=0, sticky='nsew')

        self.tree["columns"] = ("deposit_id", "item_name", "guest_name", "guest_mobile", 
                                "description", "date_deposited", 
                                "date_collected", "is_collected")
        

        # Set the first column heading text to an empty string
        self.tree.heading("#0", text="ID", anchor="w")
        self.tree.column("#0", width=0, stretch="no")

        # Bind the function to the Treeview's selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        for column in self.tree["columns"]:
            column_heading = column.replace("_", " ")
            self.tree.heading(column, text=column_heading.title(), anchor='w')
            self.tree.column(column, width=100)

        self.tree.column("deposit_id", width=0, stretch="no")
        
        # Create a Scrollbar
        scrollbar_y = tk.Scrollbar(frame1, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=2, sticky='ns')

        # Link the Scrollbar to the Listbox
        self.tree.config(yscrollcommand=scrollbar_y.set)

        # # horizontal scrollbar
        scrollbar_x = tk.Scrollbar(frame1, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        # Horizontal scroll bar for the Tree Table
        self.tree.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        frame1.columnconfigure(0, weight=1)
        frame1.rowconfigure(0, weight=1)
        
        # Button for refreshing the listbox
        frame2 = tk.Frame(lblFrameRight, padx=5, pady=5)    
        frame2.grid(row=2, column=0)
        self.button_refresh = tk.Button(frame2, text="Refresh Deposit List", 
                                        width=15, height=3,
                                        command=self.refresh, 
                                        bg='#225522',
                                        fg='#eeeeee',)
        # Button for printing Receipt
        self.button_receipt = tk.Button(frame2, text="Print Deposit Receipt", 
                                        width=15, height=3,
                                        command=self.print_deposit,
                                        bg='#552255',
                                        fg='#eeeeee',)
        self.button_all_to_csv = tk.Button(frame2, text="Print all to CSV", 
                                        width=15, height=3,
                                        command=self.print_all_to_csv,
                                        bg='#555522',
                                        fg='#eeeeee',)
        self.button_refresh.pack(side="left", padx=5)
        self.button_receipt.pack(side="left", padx=5)
        self.button_all_to_csv.pack(side="left", padx=5)

        labelframe_collect_deposit = tk.LabelFrame(lblFrameLeft, text="Item Collection",
                                                   padx=5, pady=5,
                                                   font=("arial", 12))
        labelframe_collect_deposit.grid(row=9, column=0, columnspan=2, sticky="nsew")

        self.button_collect = tk.Button(labelframe_collect_deposit, text="Collect Item",
                                        bg='#225522',
                                        fg='#eeeeee',
                                        font=("arial", 12, "bold"))
        self.button_collect.pack()

        # Set the weight of the first row to 1
        lblFrameRight.rowconfigure(1, weight=1)

        # Set the weight of all columns to 1
        num_columns = lblFrameRight.grid_size()[0]
        for col_index in range(num_columns):
            lblFrameRight.columnconfigure(col_index, weight=1)

    def refresh(self):
        all_deposits = self.model.select_all()
        
        # Clear existing data in the Treeview
        self.tree.delete(*self.tree.get_children())
        self.fill_table(all_deposits)

    def fill_table(self, data):
        # Populate the Treeview with the deposits data
        for deposit in data:
            deposit_id, guest_id, deposits_name, description, date_deposited, date_collected, is_collected, guest_first_name, guest_last_name, guest_mobile = deposit
            guest_name = f"{guest_first_name} {guest_last_name}"
            if is_collected:
                is_collected = "Yes"
            else:
                is_collected = "No"
            self.tree.insert("", "end", text= deposit_id,
                             values=(deposit_id, deposits_name, guest_name, guest_mobile,
                                     description, date_deposited, 
                                     date_collected, is_collected))
            
    def search(self):
        self.tree.delete(*self.tree.get_children())
        search_item = self.entry_search.get()
        search_by = self.combo_search_by.get()
        if search_item:
            if search_by == "GUEST PHONE NUMBER":
                rows = self.model.find_deposits_by_guest(guest_mobile=search_item)
            elif search_by == "DEPOSIT DATE":
                rows = self.model.find_by_deposit_date(deposit_date=search_item)
            elif search_by == "COLLECT DATE":
                rows = self.model.find_by_collect_date(collect_date=search_item)
            else:
                rows = None
            if rows:
                self.fill_table(rows)
            else:
                messagebox.showerror("Not Found!", "No item deposited match!")
        else:
            messagebox.showwarning("No Entry", "Enter a Value to search!")
            
    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            if values:
                deposit_id, deposit_name, collected_status = values[0], values[1], values[7]
                if collected_status == "No":
                    self.controller.populate_entry_fields(*values)
                    self.button_collect.config(text="Collect Item", bg="green", fg="white")
                    self.button_collect.bind("<Button-1>", lambda event: self.collect_item(deposit_id))
                else:
                    messagebox.showinfo("Collected", f"Item {deposit_name} has been already being collected.")
            else:
                messagebox.showinfo("No Item Deposit", f"No Item is currently deposited!")

    def collect_item(self, room_number):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            if values:
                deposit_id, deposit_name, collected_status = values[0], values[1], values[7]
                if collected_status == "No":
                    self.button_collect.config(text="Collect")
                    self.model.mark_deposit_collected(deposit_id)
                    messagebox.showinfo("Success", f"Room {deposit_name} is collected successfully.")
                    self.refresh()
                else:
                    messagebox.showinfo("Collected", f"Item {deposit_name} has been already being collected.")
        else:
            messagebox.showwarning("Warning", "Select an item to collect.")

    def print_deposit(self):
        selected_row = self.tree.selection()
        if selected_row:
            selected_item = self.tree.item(selected_row[0])
            row_data = selected_item.get("values")
            if row_data and isinstance(row_data, (list, tuple)):
                receipt = PrintDeposits(row_data)
                receipt.print_receipt()
                messagebox.showinfo("Success", "Deposit Receipt generated successfully.")
            else:
                messagebox.showwarning("Warning", "Invalid deposit data.")
        else:
            messagebox.showwarning("Warning", "Select a deposit to print.")

    def print_all_to_csv(self):
        # Get the main Documents directory for the operating system
        documents_directory = os.path.expanduser("~/Documents")

        # Create a folder called MFM_guest_house in the Documents directory
        os.makedirs(documents_directory + "/MFM_guest_house/reports", exist_ok=True)

        # Get the current date and time
        now = datetime.today()
        current_time_and_date = now.strftime("%Y%m%d_%H%M%S")

        # Create a PrintToClass object for the reservations_`current_time_and_date`.csv file
        print_to_class = PrintRecord(documents_directory + "/MFM_guest_house/deposits_" + current_time_and_date + ".csv")

        # Write the row data to the CSV file
        for row in self.tree.get_children():
            row_data = self.tree.item(row)["values"]
            print_to_class.write_row(row_data)
        messagebox.showinfo("Successfully generated", "Record has been successfully generated")

