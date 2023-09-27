import random
import sqlite3
import tkinter as tk
from tkinter import FLAT, Label, StringVar, ttk
from tkinter import messagebox

from tkinter import Button, Label, LabelFrame, RIDGE
from tkinter import ttk
import random

from models.guests_model import GuestModel


class GuestController:
    def __init__(self):
        self.model = GuestModel()

    def create_widgets(self, view, lblFrameLeft):
        lblFrameLeft.columnconfigure(0, weight=1)
        lblFrameLeft.columnconfigure(1, weight=1)

        self.var_guest_name = tk.StringVar(lblFrameLeft)
        self.var_guest_last_name = tk.StringVar(lblFrameLeft)
        self.var_guest_gender = tk.StringVar(lblFrameLeft)
        self.var_guest_next_of_kin_mobile = tk.StringVar(lblFrameLeft)
        self.var_guest_mobile = tk.StringVar(lblFrameLeft)
        self.var_guest_email = tk.StringVar(lblFrameLeft)
        self.var_guest_nationality = tk.StringVar(lblFrameLeft)
        self.var_guest_ID_TYPE = tk.StringVar(lblFrameLeft)
        self.var_guest_id_number = tk.StringVar(lblFrameLeft)
        self.var_guest_address = tk.StringVar(lblFrameLeft)

        ############### VARIABLES ###############
        self.var_ref = StringVar()
        x = random.randint(10000000000000, 99999999999999)
        self.var_ref.set(str(x))

        ############## REFRENCE NO. #################
        lbl_guest_ref = Label(lblFrameLeft, text="GUEST REF :", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_guest_ref.grid(row=0, column=0, sticky="w")
        
        entry_ref = ttk.Entry(lblFrameLeft, textvariable=self.var_ref, font=("arial",11,"bold"), state="readonly")
        entry_ref.grid(row=0, column=1, sticky="ew")

        ############## GUEST NAME ##############
        lbl_guest_name = Label(lblFrameLeft, text="FIRST NAME :", font=("arial",10,"bold"), padx=2,pady=6)
        lbl_guest_name.grid(row=1, column=0, sticky="w")
        
        entry_name = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_name, font=("arial", 11,"bold"))
        entry_name.grid(row=1, column=1, sticky="ew")

        ############# last_nameS NAME ###############
        lbl_guest_mname = Label(lblFrameLeft, text="LAST NAME :", font=("arial",10,"bold"), padx=2, pady=6)
        lbl_guest_mname.grid(row=2, column=0, sticky="w")
        
        entry_mname = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_last_name, font=("arial", 11, "bold"))
        entry_mname.grid(row=2, column=1, sticky="ew")

        ############ GENDER BOX ###############
        lbl_gender = Label(lblFrameLeft, font=("arial", 10, "bold"), text="GENDER :", padx=2, pady=6)
        lbl_gender.grid(row=3, column=0, sticky="w")
        
        combo_gender = ttk.Combobox(lblFrameLeft, textvariable=self.var_guest_gender, font=("arial", 10, "bold"), state="readonly")
        combo_gender["value"]=("MALE","FEMALE")
        combo_gender.current(0)
        combo_gender.grid(row=3, column=1, sticky="ew")

        ########### NEXT_OF_KIN_MOBILE CODE ###############
        lbl_guest_next_of_kin_mobile = Label(lblFrameLeft, text="NEXT OF KIN NO.:", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_guest_next_of_kin_mobile.grid(row=4, column=0, sticky="w")
        
        entry_next_of_kin_mobile = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_next_of_kin_mobile, width=29, font=("arial", 11, "bold"))
        entry_next_of_kin_mobile.grid(row=4, column=1, sticky="ew")

        ########## MOBILE NUMBER ##############
        lbl_guest_mob = Label(lblFrameLeft,text="MOBILE :", font=("arial",10,"bold"), padx=2,pady=6)
        lbl_guest_mob.grid(row=5, column=0, sticky="w")
        
        entry_mob = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_mobile, font=("arial", 11, "bold"))
        entry_mob.grid(row=5, column=1, sticky="ew")

        ########## EMAIL ##################
        lbl_guest_email = Label(lblFrameLeft, text="EMAIL :", font=("arial",10,"bold"), padx=2, pady=6)
        lbl_guest_email.grid(row=6, column=0, sticky="w")
        
        entry_email = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_email, font=("arial",11,"bold"))
        entry_email.grid(row=6, column=1, sticky="ew")

        ########### NATIONALITY ##############
        lblNationality = Label(lblFrameLeft,font=("arial", 10, "bold"),text="NATIONALITY :", padx=2, pady=6)
        lblNationality.grid(row=7, column=0, sticky="w")
        
        combo_nationality=ttk.Combobox(lblFrameLeft, textvariable=self.var_guest_nationality, font=("arial", 10, "bold"), width=31, state="readonly")
        combo_nationality["value"] = ("NIGERIAN", "FOREIGNER")
        combo_nationality.current(0)
        combo_nationality.grid(row=7, column=1, sticky="ew")

        ############ IDPROFF TYPE #############
        lblIdproff = Label(lblFrameLeft,font=("arial", 10, "bold"),text="ID CARD TYPE :", padx=2, pady=6)
        lblIdproff.grid(row=8, column=0, sticky="w")
        
        combo_idproff=ttk.Combobox(lblFrameLeft, textvariable=self.var_guest_ID_TYPE, font=("arial", 10, "bold"), state="readonly")
        combo_idproff["value"]=("NONE", "NATIONAL ID CARD", "PASSPORT", "DRIVING LICIENCE","VOTERS CARD", "OTHERS")
        combo_idproff.current(0)
        combo_idproff.grid(row=8, column=1, sticky="ew")

        ############ ID NUMBER #################
        lbl_guest_idno = Label(lblFrameLeft, text="ID NUMBER :", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_guest_idno.grid(row=9, column=0, sticky="w")
        
        entry_idno = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_id_number, width=29, font=("arial", 11, "bold"))
        entry_idno.grid(row=9, column=1, sticky="ew")

        ########### ADDRESS #################
        lbl_guest_addr = Label(lblFrameLeft,text="ADDRESS :", font=("arial", 10, "bold"), padx=2, pady=6)
        lbl_guest_addr.grid(row=10, column=0, sticky="w")
        
        entry_addr = ttk.Entry(lblFrameLeft, textvariable=self.var_guest_address, font=("arial",11,"bold"))
        entry_addr.grid(row=10, column=1, sticky="ew")

        ############## BUTTONS ##############
        btn_frame = LabelFrame(lblFrameLeft, relief=FLAT)
        
        btn_frame.grid(row=11, column=0, columnspan=2, sticky="ew")
        btn_frame.columnconfigure(0, weight=1)

        btn_add = Button(btn_frame, text="ADD", command=view.add_data, 
                         font=("arial",10,"bold"), bg="#222255", fg="#ffffff")
        btn_add.grid(row=0, column=0, columnspan=2, padx=5, sticky="ew")
        # btn_add.grid(row=0, column=0, padx=5, sticky="ew")

        btn_update = Button(btn_frame, text="UPDATE", command=view.update, 
                            font=("arial", 10, "bold"), bg="#225522", fg="#ffffff", width=10)
        btn_update.grid(row=0, column=2, padx=5, sticky="ew")

        btn_delete = Button(btn_frame, text="DELETE", command=view.delete,
                            bg="#552222", fg="#ffffff",
                            font=("arial", 10,"bold"))
        # btn_delete.grid(row=0, column=2, padx=5, sticky="ew")

        btn_reset = Button(btn_frame, text="RESET", command=self.data_reset,
                           bg="#222222", fg="#ffffff",
                           font=("arial",10,"bold"))
        btn_reset.grid(row=0, column=3, padx=5, sticky="ew")

    def data_reset(self):
        self.var_guest_name.set("")
        self.var_guest_last_name.set("")
        self.var_guest_gender.set("")
        self.var_guest_next_of_kin_mobile.set("")
        self.var_guest_mobile.set("")
        self.var_guest_email.set("")
        self.var_guest_nationality.set("")
        self.var_guest_ID_TYPE.set("")
        self.var_guest_id_number.set("")
        self.var_guest_address.set("")
        x = random.randint(10000000000000, 99999999999999)
        self.var_ref.set(str(x))