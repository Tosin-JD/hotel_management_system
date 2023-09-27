import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# Import the DepositModel class here
# Make sure you have the DepositModel class defined properly
from models.deposits_model import DepositModel


class DepositController:
    def __init__(self, view, root):
        self.root = root
        self.view = view
        self.model = DepositModel()

    def create_widgets(self, lblFrameLeft):
        # Create labels and entry widgets for data input
        self.label_guest_id = tk.Label(lblFrameLeft, text="Guest Phone Number:",
                                          font=("arial", 12, "bold"))
        self.entry_guest_id = tk.Entry(lblFrameLeft)

        self.label_deposits_name = tk.Label(lblFrameLeft, text="Item Name:",
                                            font=("arial", 12, "bold"))
        self.entry_deposits_name = tk.Entry(lblFrameLeft)

        self.label_description = tk.Label(lblFrameLeft, text="Description:",
                                          font=("arial", 12, "bold"))
        self.entry_description = tk.Entry(lblFrameLeft)

        self.label_date_deposited = tk.Label(lblFrameLeft, text="Date Deposited:",
                                             font=("arial", 12, "bold"))
        self.entry_date_deposited = DateEntry(lblFrameLeft, date_pattern="yyyy-mm-dd")

        self.label_date_collected = tk.Label(lblFrameLeft, text="Date Collected:",
                                             font=("arial", 12, "bold"))
        self.entry_date_collected = DateEntry(lblFrameLeft, date_pattern="yyyy-mm-dd")

        # Create buttons for CRUD operations
        self.button_add = tk.Button(lblFrameLeft, text="Add Deposit",
                                    bg='#222255',
                                    fg='#eeeeee',
                                    command=self.add_deposit)
        self.button_update = tk.Button(lblFrameLeft, text="Update Deposit", 
                                       bg='#225522',
                                       fg='#eeeeee',
                                       command=self.update)
        self.button_delete = tk.Button(lblFrameLeft, text="Delete Deposit",
                                       bg='#552222',
                                       fg='#eeeeee',
                                       command=self.delete)
        self.button_reset = tk.Button(lblFrameLeft, text="Reset", 
                                      bg='#222222',
                                      fg='#eeeeee',
                                      command=self.clear_entries)

        # Grid layout for widgets
        self.label_guest_id.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_guest_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label_deposits_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_deposits_name.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.label_description.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_description.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.label_date_deposited.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_date_deposited.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.label_date_collected.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_date_collected.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.button_add.grid(row=5, column=1, columnspan=1, padx=5, pady=5, sticky="ew")
        self.button_update.grid(row=6, column=1, columnspan=1, padx=5, pady=5, sticky="ew")
        # self.button_delete.grid(row=7, column=1, columnspan=1, padx=5, pady=5, sticky="ew")
        self.button_reset.grid(row=8, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        num_rows = lblFrameLeft.grid_size()[1]
        num_columns = lblFrameLeft.grid_size()[0]

        # Set the weight of all rows to 1
        for row_index in range(num_rows):
            lblFrameLeft.rowconfigure(row_index, weight=1)

        # Set the weight of all columns to 1
        for col_index in range(num_columns):
            lblFrameLeft.columnconfigure(col_index, weight=1)


    def clear_entries(self):
        # Clear the input fields after adding, updating, or deleting a deposit
        self.entry_guest_id.delete(0, tk.END)
        self.entry_deposits_name.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.entry_date_deposited.delete(0, tk.END)
        self.entry_date_collected.delete(0, tk.END)

    def add_deposit(self):
        # Get data from the entry fields
        guest_id = self.entry_guest_id.get()
        deposits_name = self.entry_deposits_name.get()
        description = self.entry_description.get()
        date_deposited = self.entry_date_deposited.get()
        date_collected = self.entry_date_collected.get()
        try:
            # Insert the deposit data into the database using the DepositModel class
            self.model.insert(
                guest_id, deposits_name, description, date_deposited, date_collected
            )
            messagebox.showinfo("Deposit Added", "The deposit was successfully added.")
        except ValueError:
            messagebox.showwarning("Error", "No Guest with that Phone Number. Please register the guest.")
        except Exception as e:
            messagebox.showerror("Error", f"{e}\nContact the developer!")
        finally:
            self.view.refresh()
            self.clear_entries()

    def populate_entry_fields(self, *values):
        self.entry_deposits_name.delete(0, tk.END)
        self.entry_deposits_name.insert(0, values[1])

        self.entry_guest_id.delete(0, tk.END)
        self.entry_guest_id.insert(0, values[3])
        
        self.entry_description.delete(0, tk.END)
        self.entry_description.insert(0, values[4])

        self.entry_date_deposited.delete(0, tk.END)
        self.entry_date_deposited.insert(0, values[5])

        self.entry_date_collected.delete(0, tk.END)
        self.entry_date_collected.insert(0, values[6])

    def update(self):
        selected_item = self.view.tree.selection()
        # Get data from the entry fields
        guest_id = self.entry_guest_id.get()
        deposits_name = self.entry_deposits_name.get()
        description = self.entry_description.get()
        date_deposited = self.entry_date_deposited.get()
        date_collected = self.entry_date_collected.get()

        if guest_id and deposits_name and description and date_deposited and date_collected:
            try:
                self.model.update(guest_id, deposits_name, description, date_deposited, date_collected)
                messagebox.showinfo("Deposited Item Updated", "The item has been updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"{e}\nContact the Developer.")
            finally:
                self.view.refresh()
        else:
            messagebox.showwarning("Error", "Please fill in all the required fields.")

        # Clear the input fields
        self.clear_entries()

    def delete(self):
        selected_item = self.view.tree.selection()
        if selected_item:
            selected_item = self.view.tree.item(selected_item, "values")
            response = messagebox.askyesno("Confirmation", 
                                           f"""Do you want to delete {selected_item[1]}?""")
            if response:
                try:
                    self.model.delete(selected_item[0])
                    messagebox.showinfo("Delete Successful", f"{selected_item[1]} has been deleted.")
                except Exception as e:
                    messagebox.showerror("Error", f"{e}\nContact the developer!")
                finally:
                    self.clear_entries()
                    self.view.refresh()
            else:
                # Perform the action for 'No' choice 
                messagebox.showinfo("Canceled", "Deletion operation canceled.")             
        else:
            messagebox.showwarning("Error", "Please select an item to delete.")
        


if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Create an instance of the DepositController class
    deposit_controller = DepositController(root)

    # Start the tkinter event loop
    root.mainloop()
