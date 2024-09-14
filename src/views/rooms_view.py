import tkinter as tk
from tkinter import BOTH, BOTTOM, HORIZONTAL, NO, RIGHT, VERTICAL, X, Y, messagebox
from tkinter import ttk
from models.rooms_model import RoomModel
from controllers.rooms_controllers import RoomController


class RoomView:
    def __init__(self, root):
        self.root = root
        self.model = RoomModel()
        self.controller = RoomController(self, self.root)
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=5)
        self.root.rowconfigure(1, weight=5)
        ################ Title ##################
        lbl_title = tk.Label(self.root, text="ROOMS", 
                             bg="#222222", fg="#eeeeee",
                             font=("arial", 18, "bold"), padx=2, 
                             border=4, relief="flat")
        lbl_title.grid(row=0, column=0, columnspan=2, sticky='ew')

        lblFrameRight = tk.LabelFrame(self.root, bd=2, 
                                      relief="flat", 
                                      text="ROOMS DETAILS", 
                                      font=("arial", 12, "bold"))
        lblFrameRight.grid(row=1, column=1, sticky="nsew")
        lblFrameRight.columnconfigure(0, weight=1)

        # Constructing the first frame, frame1
        frame1 = tk.Frame(lblFrameRight)    
        search_frame = tk.Frame(lblFrameRight, pady=5)    
        search_frame.grid(row=0, column=0, sticky='ew')
        lbl_search = tk.Label(search_frame, text="Search For Room by Room Number", font=("arial", 12, "bold"))
        self.entry_search = tk.Entry(search_frame, width=10, font=("arial", 14, "bold"))
        btn_search = tk.Button(search_frame, text="Search", bg="#222255", 
                               fg="#eeeeee", font=("arial", 12, "bold"),
                               command=self.search)
        btn_get_reserved = tk.Button(search_frame, text="Get Reserved Rooms", bg="#225522", 
                               fg="#eeeeee", font=("arial", 12, "bold"),
                               command=self.get_reserved)
        btn_get_unreserved = tk.Button(search_frame, text="Get Unreserved Rooms", bg="#552222", 
                               fg="#eeeeee", font=("arial", 12, "bold"),
                               command=self.get_unreserved)
        
        btn_show_all = tk.Button(search_frame, text="Show All", bg="#222222", fg="#eeeeee", font=("arial", 12, "bold"), command=self.refresh)

        lbl_search.grid(row=0, column=0, padx=5, sticky='nsew')
        self.entry_search.grid(row=0, column=1, pady=5, padx=5, sticky='nsew')
        btn_search.grid(row=0, column=2, padx=5, sticky='nsew')
        btn_get_reserved.grid(row=0, column=3, padx=5, sticky='nsew')
        btn_get_unreserved.grid(row=0, column=4, padx=5, sticky='nsew')
        btn_show_all.grid(row=0, column=5, padx=5, sticky='nsew')

        frame1.grid(row=1, column=0, sticky='nsew')
        
        self.tree = ttk.Treeview(frame1, columns=("Room ID", "Room Name", "Room Category", "Price", "Reserved"), show="headings")
        self.tree.heading("Room ID", text="Room ID", anchor='w')
        self.tree.heading("Room Name", text="Room Name", anchor='w')
        self.tree.heading("Room Category", text="Room Category", anchor='w')
        self.tree.heading("Price", text="Price", anchor='w')
        self.tree.heading("Reserved", text="Reserved", anchor='w')

        # Adjust column widths to fit content
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("Room ID", stretch=0, width=0)
        self.tree.column("Room Name", width=150)
        self.tree.column("Room Category", width=120)
        self.tree.column("Price", width=100)
        self.tree.column("Reserved", width=80)

        # Bind the function to the Treeview's selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        
        # Constructing the second frame, frame2
        frame2 = tk.Frame(lblFrameRight, padx=5)
                
        # Displaying the frame2 in row 0 and column 1
        frame2.grid(row=2, column=0)

        # Create a Scrollbar
        scrollbar_y = tk.Scrollbar(frame1, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the Scrollbar to the Listbox
        self.tree.config(yscrollcommand=scrollbar_y.set)

        # # horizontal scrollbar
        scrollbar_x = tk.Scrollbar(frame1, orient=tk.HORIZONTAL, command=self.tree.xview)

        # Horizontal scroll bar for the Tree Table
        self.tree.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill="both", expand=True)

        # Button for refreshing the listbox
        self.button_refresh = tk.Button(frame2, text="Refresh", 
                                         bg='#225522',
                                         fg='#eeeeee',
                                         width=15, height=3,
                                         command=self.refresh)
        self.button_refresh.pack()

        # make the content fit horizontally
        lblFrameRight.rowconfigure(1, weight=1)
        

    def refresh(self):
        # Clear the Treeview if it's not empty
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())
        all_rooms = self.model.select_all_rooms()
        self.fill_table(all_rooms)

    def get_reserved(self):
        # Clear the Treeview if it's not empty
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())
        rooms = self.model.get_reserved()
        self.fill_table(rooms)

    def get_unreserved(self):
        # Clear the Treeview if it's not empty
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())
        rooms = self.model.get_unreserved()
        self.fill_table(rooms)
    
    def fill_table(self, data):
        for room in data:
            room_id, room_name, room_category, room_price, is_available = room
            is_available_text = "Yes" if is_available else "No"
            self.tree.insert("", "end",
                                   values=(room_id, f"Room {room_name}",
                                    room_category, 
                                    room_price,
                                    is_available_text))
            
    def search(self):
        self.tree.delete(*self.tree.get_children())
        room_number = self.entry_search.get()
        if room_number:
            try:
                rows = self.model.get_rooms_by_number(room_number=room_number)
                if rows:
                    self.fill_table(rows)
                else:
                    messagebox.showerror("Not Found!", "No room with this number exists")
            except Exception as e:
                messagebox.showerror("Error", f"{e}\nContact the developer!")
        else:
            messagebox.showwarning("No Entry", "Enter a room number to search!")
            
    def on_row_select(self, event):
        selected_row = self.tree.selection()
        if selected_row:
            reserved_status = self.tree.item(selected_row)["values"][4]
        if reserved_status == "Yes":
            self.controller.button_reserve_or_unreserve_room.config(text="Unreserve")
        else:
            self.controller.button_reserve_or_unreserve_room.config(text="Reserve")
         
    # Define the selection event handler
    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            if values:
                room_number, room_category, room_price, reserved_status = values[1], values[2], values[3], values[4]
                room_number = str(room_number[5:])
                self.controller.populate_entry_fields(room_number, room_category, room_price)
                if reserved_status == "Yes":
                    self.controller.button_reserve_or_unreserve_room.config(text="Unreserve", bg="green", fg="white")
                    self.controller.button_reserve_or_unreserve_room.bind("<Button-1>", lambda event: self.controller.reserve_or_unreserve(room_number))
                else:
                    self.controller.button_reserve_or_unreserve_room.config(text="Reserve", bg="red", fg="white")
                    self.controller.button_reserve_or_unreserve_room.bind("<Button-1>", lambda event: self.controller.reserve_or_unreserve(room_number))
