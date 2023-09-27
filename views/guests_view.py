import random
import sqlite3
import tkinter as tk
from tkinter import Label, StringVar, ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from tkinter import*
from PIL import Image, ImageTk #pip install pillow
from tkinter import ttk
import random

from controllers.guests_controller import GuestController


from models.guests_model import GuestModel

class GuestView:
    def __init__(self, root):
        self.root = root
        self.model = GuestModel()
        self.controller = GuestController()
        root.grid_columnconfigure(0, weight=10, minsize=400)
        root.grid_columnconfigure(1, weight=5, minsize=700)
        root.rowconfigure(1, weight=5)
        ################ Title ##################

        lbl_title = Label(
            self.root,
            text="GUESTS",
            font=("arial", 18, "bold"),
            bg="#222222", fg="#eeeeee",
            bd=4, relief=FLAT
        )
        
        lbl_title.grid(row=0, column=0, columnspan=2, sticky='ew')

        ################ LABEL FRAME ###################
        self.lblFrameLeft = tk.LabelFrame(self.root, width=400, bd=2, 
                                          relief=FLAT, text="GUESTS DETAILS", 
                                          font=("arial", 12, "bold"), padx=2)
        self.lblFrameLeft.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lblFrameLeft.grid_columnconfigure(0, weight=1)
        self.lblFrameLeft.grid_columnconfigure(1, weight=2)
        
        lblFrameRight = tk.LabelFrame(self.root, bd=2, relief=FLAT, text="SEARCH AND VIEW DETAILS",
                                      font=("arial",12,"bold"), padx=2)
        lblFrameRight.grid(row=1, column=1, sticky="nsew")

        ################ CONTROLLER ###################
        self.controller.create_widgets(self, self.lblFrameLeft)

        ############## TABLE FRAME SEARCH ###############        

        lblsearchby = tk.Label(lblFrameRight, text="SEARCH BY :",font=("arial",12,"bold"),bg="red",fg="white")
        lblsearchby.grid(row=0, column=0, sticky="W", padx=4)

        self.search_var = StringVar()

        combo_search = ttk.Combobox(lblFrameRight, textvariable=self.search_var, font=("arial",12,"bold"), width=12, state="readonly")
        combo_search["value"]=("MOBILE","REF_NO")
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=4)

        self.txt_search = StringVar()
        entry_search = ttk.Entry(lblFrameRight, textvariable=self.txt_search, width=20, 
                                 font=("arial", 12), foreground="black")
        entry_search.grid(row=0, column=2, padx=4)

        btn_search = Button(lblFrameRight, text="SEARCH", command=self.search_data, font=("arial",12,"bold"), bg="#222222",fg="#eeeeee",width=10)
        btn_search.grid(row=0,column=3, padx=5)

        btn_showall = Button(lblFrameRight, text="SHOW ALL!!", command=self.fetch_data, font=("arial",12,"bold"), bg="#222222",fg="#eeeeee",width=10)
        btn_showall.grid(row=0, column=4, padx=5)

        ################ SHOW DATA TABLE ##############
        table_frame = Label(lblFrameRight, bd=2, relief=FLAT, width=300)
        table_frame.grid(row=1, column=0, columnspan=5, sticky="nsew") 
        self.tree = ttk.Treeview(table_frame,columns=("REF_NO",
                                                                    "FIRST_NAME",
                                                                    "LAST_NAME",
                                                                    "GENDER",
                                                                    "NEXT_OF_KIN_MOBILE",
                                                                    "MOBILE","EMAIL",
                                                                    "NATIONALITY",
                                                                    "ID_TYPE",
                                                                    "ID_NO",
                                                                    "ADDRESS"),
                                                                    )
        self.tree["columns"] = ("REF_NO",
                                            "FIRST_NAME",
                                            "LAST_NAME",
                                            "GENDER",
                                            "NEXT_OF_KIN_MOBILE",
                                            "MOBILE","EMAIL",
                                            "NATIONALITY",
                                            "ID_TYPE",
                                            "ID_NO",
                                            "ADDRESS")
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        for column in self.tree["columns"]:
            column_heading = column.replace("_", " ")
            self.tree.heading(column, text=column_heading.title(), anchor='w')
            self.tree.column(column, width=100)
        
        Scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.tree.config(xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)

        Scroll_x.pack(side=BOTTOM, fill=X)
        Scroll_y.pack(side=RIGHT, fill=Y)

        Scroll_x.config(command=self.tree.xview)
        Scroll_y.config(command=self.tree.yview)

        self.tree["show"] = "headings"

        self.tree.pack(fill="both", expand=True)
        self.fetch_data()

        num_columns = lblFrameRight.grid_size()[0]

        # lblFrameRight.rowconfigure(0, weight=1)
        lblFrameRight.rowconfigure(1, weight=2)
        
        # Set the weight of all columns to 1
        for col_index in range(num_columns):
            lblFrameRight.columnconfigure(col_index, weight=5)

    def add_data(self):
        if self.controller.var_guest_mobile.get() == "" or self.controller.var_guest_last_name.get() == "":
            messagebox.showerror("Error", "ALL FIELDS ARE REQUIRED!!! \nGuest must have a phone number!", parent=self.root)
        else:
            first_name = self.controller.var_guest_name.get()
            last_name = self.controller.var_guest_last_name.get()
            guest_data = [
                first_name.upper(),
                last_name.upper(),
                self.controller.var_guest_gender.get(),
                self.controller.var_guest_next_of_kin_mobile.get(),
                self.controller.var_guest_mobile.get(),
                self.controller.var_guest_email.get(),
                self.controller.var_guest_nationality.get(),
                self.controller.var_guest_ID_TYPE.get(),
                self.controller.var_guest_id_number.get(),
                self.controller.var_guest_address.get(),
            ]
            try:
                self.model.add_guest(guest_data)
                messagebox.showinfo("Success", "Guest has been added", parent=self.root)
                self.controller.data_reset()
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Error", f"{e}\nA guest with this Mobile number already exists.")
            except Exception as e:
                messagebox.showerror("Error", f"{e}\nContact the developer!")
            finally:
                self.fetch_data()

    def fetch_data(self):
        rows = self.model.get_guests()
        # Clear the Treeview if it's not empty
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())
        for item in rows:
            item = item[1:]
            self.tree.insert("", tk.END, values=item)

    def search_data(self):
        rows = self.model.search_guests(
            str(self.search_var.get()), str(self.txt_search.get())
        )
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())
        for item in rows:
            item = item[1:]
            self.tree.insert("", tk.END, values=item)

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = [str(value) for value in self.tree.item(selected_item)["values"]]
            values[4] = "0" + values[4]
            values[5] = "0" + values[5]
            self.populate_entry_fields(*values)

    def populate_entry_fields(self, *values):
        self.controller.var_ref.set(str(values[0]))
        self.controller.var_guest_name.set(str(values[1]))
        self.controller.var_guest_last_name.set(str(values[2]))
        self.controller.var_guest_gender.set(str(values[3]))
        self.controller.var_guest_next_of_kin_mobile.set(str(values[4]))     
        self.controller.var_guest_mobile.set(str(values[5])) 
        self.controller.var_guest_email.set(str(values[6]))
        self.controller.var_guest_nationality.set(str(values[7]))
        self.controller.var_guest_ID_TYPE.set(str(values[8]))
        self.controller.var_guest_id_number.set(str(values[9]))
        self.controller.var_guest_address.set(str(values[10]))

    def update(self):
        if self.controller.var_guest_mobile.get() == "":
            messagebox.showerror("Error", "Please enter mobile number", parent=self.root)
        else:
            first_name = self.controller.var_guest_name.get()
            last_name = self.controller.var_guest_last_name.get()
            guest_data = [
                first_name.upper(),
                last_name.upper(),
                self.controller.var_guest_gender.get(),
                self.controller.var_guest_next_of_kin_mobile.get(),
                self.controller.var_guest_mobile.get(),
                self.controller.var_guest_email.get(),
                self.controller.var_guest_nationality.get(),
                self.controller.var_guest_ID_TYPE.get(),
                self.controller.var_guest_id_number.get(),
                self.controller.var_guest_address.get(),
                self.controller.var_ref.get(),
            ]
            try:
                self.model.update_guest(guest_data)
                messagebox.showinfo("Update", "Guest details have been updated successfully", parent=self.root)
                self.fetch_data()
            except sqlite3.IntegrityError as e:
                 messagebox.showerror("Error", f"{e}\nA guest with this Mobile number already exists.")
            finally:
                self.fetch_data()

    def delete(self):
        ref_no = self.controller.var_ref.get()
        if ref_no:
            result = messagebox.askyesno("Delete Guest Data", "Do you want to delete this guest's data?", parent=self.root)
            if result:
                self.model.delete(ref_no)
                self.fetch_data()
                messagebox.showinfo("Delete Successful", "Guest data has been deleted successfully.", parent=self.root)
        else:
            messagebox.showwarning("Warning", "Please select a guest to delete", parent=self.root)