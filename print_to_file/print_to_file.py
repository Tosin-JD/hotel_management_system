import os
import csv
import os
from datetime import datetime

from reportlab.lib.pagesizes import A5
from reportlab.pdfgen.canvas import Canvas


class PrintRecord:
    def __init__(self, filename):
        self.filename = filename
        self.csvwriter = csv.writer(open(filename, "w", newline=''))

    def write_row(self, row_data):
        self.csvwriter.writerow(row_data)


class PrintReceipt:
    def __init__(self, reservation_data):
        self.reservation_data = reservation_data

    def convert_amount_to_float(self, amount_str):
        try:
            return float(amount_str.replace(',', ''))
        except ValueError:
            return 0.0

    def draw_horizontal_line(self, y_position):
        self.c.line(20, y_position, 550, y_position)

    def print_receipt(self):
        # Get the main Documents directory for the operating system
        documents_directory = os.path.expanduser("~/Documents")

        # Create a folder called MFM_guest_house in the Documents directory
        os.makedirs(documents_directory + "/MFM_guest_house/receipts", exist_ok=True)
        
        #  Get the current date and time
        now = datetime.today()
        current_time_and_date = now.strftime("%Y%m%d_%H%M%S")

        self.c = Canvas(
                        documents_directory + "/MFM_guest_house/receipts/receipt_" +
                        self.reservation_data[1] + " " +
                        current_time_and_date + ".pdf"
                        )
        self.c.setFont("Helvetica-Bold", size=40)
        self.c.setFillColorRGB(0.7, 0.7, 0.7)  # Light gray color for the watermark
        self.c.rotate(45)  # Rotate the watermark
        self.c.drawString(250, 200, "MFM GUEST HOUSE UTAKO ABUJA")
        self.c.rotate(-45)  # Reset the rotation
        self.c.setFillColorRGB(0, 0, 0)  # Reset the fill color to black

        #PAID
        self.c.setFont("Helvetica-Bold", size=40)
        self.c.setFillColorRGB(0.0, 0.5, 0.3)  # Light gray color for the watermark
        # self.c.rotate(45)  # Rotate the watermark
        self.draw_horizontal_line(215)
        self.c.drawString(240, 180, "PAID")
        self.draw_horizontal_line(175)
        # self.c.rotate(-45)  # Reset the rotation
        self.c.setFillColorRGB(0, 0, 0)  # Reset the fill color to black
        
        self.c.setFont("Helvetica", size=20)
        # Title and full Reservation Receipt
        self.c.drawString(150, 800, "MFM Guest House Utako, Abuja")
        self.c.setFont("Helvetica-Bold", size=20)
        self.c.drawString(200, 750, "Reservation Receipt")

        # Current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.setFont("Helvetica", size=12)
        self.c.drawString(400, 30, "Printed: " + current_datetime)

        phone_number = ["+234 913 619 9008", "+234 906 416 0580", "mfmghutako@gmail.com"]
        self.c.setFont("Helvetica", size=12)
        self.c.drawString(20, 150, "Phone Number 1: " + phone_number[0])
        self.c.drawString(20, 130, "Phone Number 2: " + phone_number[1])
        self.c.drawString(20, 110, "Email: " + phone_number[2])

        self.c.setFont("Helvetica", size=16)

        fields = [
            ("Reservation ID", str(self.reservation_data[0])),
            ("Guest Name", str(self.reservation_data[1])),
            ("Address", str(self.reservation_data[2])),
            ("Phone Number", str(self.reservation_data[3])),
            ("Suite/Hall Number", str(self.reservation_data[4])),
            ("Purpose", str(self.reservation_data[5])),
            ("Amount Paid in Naira", self.convert_amount_to_float(self.reservation_data[6])),
            ("Amount Paid In Words", str(self.reservation_data[7])),
            ("Payment Type", str(self.reservation_data[8])),
            ("Check In Date", str(self.reservation_data[9])),
            ("Check Out Date", str(self.reservation_data[10])),
        ]

        y_position = 700
        for label, value in fields:
            self.c.drawString(30, y_position, f"{label}: {value}")
            self.draw_horizontal_line(y_position - 10)
            y_position -= 30

        self.c.save()


class PrintDeposits:
    def __init__(self, reservation_data):
        self.reservation_data = reservation_data

    def convert_amount_to_float(self, amount_str):
        try:
            return float(amount_str.replace(',', ''))
        except ValueError:
            return 0.0

    def draw_horizontal_line(self, y_position):
        self.c.line(20, y_position, 550, y_position)

    def print_receipt(self):
        # Get the main Documents directory for the operating system
        documents_directory = os.path.expanduser("~/Documents")

        # Create a folder called MFM_guest_house in the Documents directory
        os.makedirs(documents_directory + "/MFM_guest_house/deposits", exist_ok=True)
        
        #  Get the current date and time
        now = datetime.today()
        current_time_and_date = now.strftime("%Y%m%d_%H%M%S")

        self.c = Canvas(
                        documents_directory + "/MFM_guest_house/deposits/deposit_" +
                        self.reservation_data[1] + " " +
                        current_time_and_date + ".pdf"
                        )
        self.c.setFont("Helvetica-Bold", size=40)
        self.c.setFillColorRGB(0.7, 0.7, 0.7)  # Light gray color for the watermark
        self.c.rotate(45)  # Rotate the watermark
        self.c.drawString(250, 200, "MFM GUEST HOUSE UTAKO ABUJA")
        self.c.rotate(-45)  # Reset the rotation
        self.c.setFillColorRGB(0, 0, 0)  # Reset the fill color to black
        
        self.c.setFont("Helvetica", size=20)
        # Title and full Reservation Receipt
        self.c.drawString(150, 800, "MFM Guest House Utako, Abuja")
        self.c.setFont("Helvetica-Bold", size=20)
        self.c.drawString(200, 750, "Deposits Receipt")

        # Current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.setFont("Helvetica", size=12)
        self.c.drawString(400, 30, "Printed: " + current_datetime)

        phone_number = ["+234 913 619 9008", "+234 906 416 0580", "mfmghutako@gmail.com"]
        self.c.setFont("Helvetica", size=12)
        self.c.drawString(20, 150, "Phone Number 1: " + phone_number[0])
        self.c.drawString(20, 130, "Phone Number 2: " + phone_number[1])
        self.c.drawString(20, 110, "Email: " + phone_number[2])

        self.c.setFont("Helvetica", size=16)

        fields = [
            ("Deposit ID", str(self.reservation_data[0])),
            ("Item Name", str(self.reservation_data[1])),
            ("Guest Name", str(self.reservation_data[2])),
            ("Description of Item", str(self.reservation_data[3])),
            ("Date Deposited", str(self.reservation_data[4])),
            ("Date Collected", str(self.reservation_data[5])),
            ("Collected", str(self.reservation_data[6])),
        ]

        y_position = 700
        for label, value in fields:
            self.c.drawString(30, y_position, f"{label}: {value}")
            self.draw_horizontal_line(y_position - 10)
            y_position -= 30

        self.c.save()
