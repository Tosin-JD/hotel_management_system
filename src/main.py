import tkinter as tk
from tkinter import FLAT
from tkinter import ttk
from views.exit_view import LicenseDisplayView, license_text
from views.guests_view import GuestView
from views.rooms_view import RoomView
from views.reservations_view import ReservationView
from views.deposits_view import DepositView
from views.hotel_status import HotelStatusView

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Guest House ")
        root.state('zoomed')
        # self.root.geometry("1600x700+0+0")
        width= self.root.winfo_screenwidth()               
        height= self.root.winfo_screenheight()               
        root.geometry("%dx%d" % (width, height))
        self.root.minsize(height=700, width=1300)
        
        ################ Title ##################
        lbl_title = tk.Label(self.root, text="GUEST HOUSE ", 
                              font=("arial", 40, "bold"), 
                              background="#222222", foreground="#eeeeee", 
                              border=0, relief=FLAT)
        lbl_title.pack(fill=tk.X)

        ################ MAIN FRAME ###############
        self.main_frame = ttk.Frame(self.root, border=4, relief=FLAT)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        ################## FORM FRAME ################
        self.form_frame = ttk.Frame(self.main_frame, border=4, relief=FLAT)
        self.form_frame.grid(row=0, column=0, sticky="nsew")

        ###################    STYLE FOR THE FONT TABS  ######################
        self.style = ttk.Style()
        self.style.configure("Tab.TNotebook", tabmargins=[2, 5, 2, 0])  # Adjust margins if needed

        ################## NOTEBOOK (TABS) ################
        self.notebook = ttk.Notebook(self.form_frame, style="Tab.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        ############## TAB 1: GUEST VIEW ##################
        self.guest_tab = ttk.Frame(self.notebook)
        self.guest_tab.columnconfigure(0, weight=2)
        self.guest_tab.rowconfigure(0, weight=1)
        self.guest_tab.rowconfigure(1, weight=2)
        self.notebook.add(self.guest_tab, text="Guests")
        self.app_guest = GuestView(self.guest_tab)

        # Change font size of the tab text
        self.style.configure("TNotebook.Tab", font=("Helvetica", 20))

        ############## TAB 2: ROOMS VIEW ##################
        self.rooms_tab = ttk.Frame(self.notebook)
        self.rooms_tab.columnconfigure(0, weight=1)
        self.rooms_tab.rowconfigure(0, weight=1)
        self.rooms_tab.rowconfigure(1, weight=2)
        self.notebook.add(self.rooms_tab, text="Rooms")
        self.app_rooms = RoomView(self.rooms_tab)

        ############## TAB 3: RESERVATIONS VIEW ##################
        self.reservations_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reservations_tab, text="Reservations")
        self.reservations_tab.columnconfigure(0, weight=1)
        self.reservations_tab.rowconfigure(0, weight=1)
        self.reservations_tab.rowconfigure(1, weight=2)
        self.app_reservations = ReservationView(self.reservations_tab)

        ############## TAB 4: DEPOSITS VIEW ##################
        self.deposits_tab = ttk.Frame(self.notebook)
        self.deposits_tab.columnconfigure(0, weight=1)
        self.deposits_tab.columnconfigure(0, weight=1)
        self.deposits_tab.rowconfigure(0, weight=1)
        self.deposits_tab.rowconfigure(1, weight=2)
        self.notebook.add(self.deposits_tab, text="Deposits")
        self.app_deposits = DepositView(self.deposits_tab)

        ############## TAB 5: EXIT ##################
        self.exit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exit_tab, text="Exit")
        exit_button = tk.Button(self.exit_tab, text="Logout",
                                 relief="flat",
                                 bg='#cc1111',
                                 fg='#eeeeee',
                                 command=self.logout)
        exit_button.pack(pady=5)
        self.app_exit = LicenseDisplayView(self.exit_tab, license_text=license_text)

        ################ MAIN FRAME ###############
        self.status_frame = ttk.Frame(self.main_frame, height=200, relief=FLAT)
        self.hotel_status = HotelStatusView(self.status_frame)
        self.status_frame.grid(row=1, column=0, sticky="ew")

    def logout(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Obj = HotelManagementSystem(root)
    root.mainloop()
