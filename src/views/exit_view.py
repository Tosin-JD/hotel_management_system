import tkinter as tk
from tkinter.scrolledtext import ScrolledText

license_text = """HOTEL MANAGEMENT SYSTEM License

 The MIT License (MIT)

Copyright © 2024 OLUWATOSIN JOSEPH DURODOLA

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE..

Licensor: DURODOLA OLUWATOSIN JOSEPH
Licensor Phone Number: +234 903 646 1479
Licensor Email Address: oluwatosinjosephdurodola@gmail.com
Licensee:  GUEST HOUSE SYSTEM"""

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

