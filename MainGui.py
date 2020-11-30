import tkinter as tk
from tkinter import ttk

import tkcalendar as tkcal

#override _select method in DateEntry.py to fit api grab date format

class CustomDateEntry(tkcal.DateEntry):

    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%Y%m%d'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()


#Create class mainGui as instance of tk.Tk
class MainGui(tk.Tk):

    def __init__(self):
        super().__init__()

        #set title
        self.title("Covid Data")

        #set dimensions
        self.geometry('500x250')

        # label text for title
        ttk.Label(self, text="Covid Data Grabber",
                  background='green', foreground="white",
                  font=("Times New Roman", 15)).grid(row=0, column=1)

        # Create Region and Date Labels
        ttk.Label(self, text="Select the Region :",
                  font=("Times New Roman", 10)).grid(column=0,
                                                     row=5, padx=10, pady=25, sticky = tk.W)

        ttk.Label(self, text="Select the date :",
                  font=("Times New Roman", 10)).grid(column=0,
                                                     row=10, padx=10, pady=25, sticky = tk.W)

        #make region dropdown menu
        n = tk.StringVar()
        region = ttk.Combobox(self, width=15, textvariable=n)

        # Adding combobox drop down list
        region['values'] = ("US", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY")

        region.grid(column=1, row=5, sticky = tk.W)
        #set default to first region
        region.current(0)


        #create cal
        cal = CustomDateEntry(self, width=15, bg="darkblue", fg="white", year=2020)

        cal.grid(column=1, row=10, sticky = tk.W)

        #create submit button

        print(cal.selection_get())

        btn = ttk.Button(self, text='Get Data',
                     command=print(12))

        # Set the position of button on the top of window.
        btn.grid(column=1, row=15, sticky = tk.W)


if __name__ == "__main__":
    maingui = MainGui()
    maingui.mainloop()