from tkinter import *
from tkinter import ttk
from views.guests_view import GuestView
from views.rooms_view import RoomView
from views.reservations_view import ReservationView
from views.deposits_view import DepositView
from views.hotel_status import HotelStatusView

from TKinterModernThemes import ThemedTKinterFrame

class HotelManagementSystem(ThemedTKinterFrame):
    def __init__(self, root, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        self.root = root
        self.root.title("MFM Guest House Utako")
        # self.root.geometry("1600x700+0+0")
        width= self.root.winfo_screenwidth()               
        height= self.root.winfo_screenheight()               
        root.geometry("%dx%d" % (width, height))
        self.root.minsize(height=700, width=1300)
        
        ################ Title ##################
        lbl_title = Label(self.root, text="MFM GUEST HOUSE UTAKO", font=("arial", 40, "bold"), bg="black", fg="gold", bd=4, relief=FLAT)
        lbl_title.pack(fill=X)

        ################ MAIN FRAME ###############
        self.main_frame = Frame(self.root, bd=4, relief=FLAT)
        self.main_frame.pack(fill=BOTH, expand=True)

        ################## FORM FRAME ################
        self.form_frame = Frame(self.main_frame, bd=4, relief=FLAT)
        self.form_frame.pack(fill=BOTH, expand=True)

        ###################    STYLE FOR THE FONT TABS  ######################
        self.style = ttk.Style()
        self.style.configure("Tab.TNotebook", tabmargins=[2, 5, 2, 0])  # Adjust margins if needed

        ################## NOTEBOOK (TABS) ################
        self.notebook = ttk.Notebook(self.form_frame, style="Tab.TNotebook")
        self.notebook.pack(fill=BOTH, expand=True)

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

        # Add any additional content you want on the Exit tab
        # For example, a button to handle logout:
        exit_button = Button(self.exit_tab, text="Logout", 
                             command=self.logout, bg='red', fg='white')
        exit_button.pack()

        ################ MAIN FRAME ###############
        self.status_frame = Frame(self.main_frame, height=300, bd=4, relief=FLAT)
        self.hotel_status = HotelStatusView(self.status_frame)
        self.status_frame.pack(fill=BOTH, expand=True)

    def logout(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    Obj = HotelManagementSystem(root, "park", "light")
    # HotelManagementSystem("park", "light")
    root.mainloop()


