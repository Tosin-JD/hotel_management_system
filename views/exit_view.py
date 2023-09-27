import tkinter as tk
from tkinter.scrolledtext import ScrolledText

license_text = """HOTEL MANAGEMENT SYSTEM License

This license agreement ("Agreement") is entered into between DURODOLA OLUWATOSIN JOSEPH ("Licensor") and the entity purchasing this license ("Licensee").

1. Grant of License:
   Licensor grants Licensee a non-transferable, non-exclusive license to use the HOTEL MANAGEMENT SYSTEM ("Software") solely for internal use within Licensee's organization.

2. Restrictions:
   Licensee shall not:
   a. Distribute, sublicense, or make the Software available to any third party.
   b. Modify, reverse engineer, decompile, or create derivative works based on the Software.

3. Ownership:
   All intellectual property rights, title, and interest in the Software remain with Licensor.

4. Support and Updates:
   Licensee may be eligible for support and updates as outlined in the purchased license package.

5. Disclaimer of Warranty:
   The Software is provided "as is," without warranty of any kind, express or implied.

6. Limitation of Liability:
   Licensor shall not be liable for any direct, indirect, incidental, special, or consequential damages arising from the use of the Software.

7. Termination:
   This Agreement may be terminated by Licensor if Licensee breaches any terms herein.

8. Governing Law:
   This Agreement shall be governed by the laws of [Jurisdiction], without regard to its conflict of law principles.

By using the Software, Licensee agrees to be bound by the terms of this Agreement.

Date: 18TH AUGUST, 2023
Licensor: DURODOLA OLUWATOSIN JOSEPH
Licensor Phone Number: +234 903 646 1479
Licensor Email Address: oluwatosinjosephdurodola@gmail.com
Licensee: MFM GUEST HOUSE UTAKO"""

class LicenseDisplayView:
    def __init__(self, root, license_text):
        self.root = root
        self.license_text = license_text
        
        self.create_widgets()
    
    def create_widgets(self):
        self.scroll_text = ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.scroll_text.pack(padx=10, pady=10)
        
        self.scroll_text.insert(tk.END, self.license_text)
        self.scroll_text.config(state=tk.DISABLED)  # Make the text widget read-only

