import tkinter as tk
from tkinter import ttk
import Overrides
import Main
from datetime import date
import tktable

#Create class mainGui as instance of tk.Tk
class MainGui(tk.Tk):

    def __init__(self):
        super().__init__()

        #set instance variable for data
        self.dataDict = None

        #set title
        self.title("Covid Data")

        #set dimensions
        self.geometry('1000x500')

        # label text for title
        ttk.Label(self, text="Covid Data Grabber",
                  background='green', foreground="white",
                  font=("Times New Roman", 15)).grid(row=0, column=1)

        #Create frame for drop-down menus and button
        inputFrame = ttk.Frame(self, relief = tk.SUNKEN, borderwidth = 2)
        outputFrame = ttk.Frame(self, relief = tk.SUNKEN, borderwidth = 2)


        inputFrame.grid(row=16, column=1, rowspan = 15, columnspan = 1, padx=10, pady=10, sticky = tk.W)
        outputFrame.grid(row = 1, column = 1, rowspan = 15, columnspan = 1, padx = 10, pady = 10, sticky = tk.W)

        # Create Region and Date Labels
        ttk.Label(inputFrame, text="Select the Region :",
                  font=("Times New Roman", 10), width=20).grid(column=0,
                                                     row=5, padx=10, pady=25, sticky = tk.W)

        ttk.Label(inputFrame, text="Select the date :",
                  font=("Times New Roman", 10), width=20).grid(column=0,
                                                     row=8, padx=10, pady=25, sticky = tk.W)

        #make region dropdown menu
        n = tk.StringVar()
        region = ttk.Combobox(inputFrame, width=20, textvariable=n)

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

        d = tk.StringVar()

        cal = Overrides.CustomDateEntry(inputFrame, textvariable = d, date_pattern='yyyymmdd', width=20, bg="darkblue", fg="white", year=2020)

        cal.grid(column=1, row=8, sticky = tk.W)

        #create submit button

        def getData():
            Main.lowerStringVar(n)
            regionString = n.get()

            if d.get() == date.today().strftime("%Y%m%d"):
                dateString = 'current'
            else:
                dateString = d.get()

            #set instance variable dataDict to the grabbed covid data
            self.dataDict = Main.getCovidData(dateString,regionString)

            #turn keys into a list
            labelList = []
            for key in self.dataDict.keys():
                labelList.append(key)

            #Add labels in data table
            labels = labelList

            for x in range(len(labels)):
                var = tk.StringVar()
                label = tk.Label(outputFrame, textvariable=var, width=20, anchor = tk.W)
                var.set(labels[x])
                label.grid(column=1, padx=10, row=2 * x + 1, sticky=tk.W, columnspan=1)

                out = tk.StringVar()
                output = tk.Entry(outputFrame, textvariable=out, width=22)
                out.set(self.dataDict[labels[x]])
                output.grid(column=2, padx=10, row=2 * x + 1, sticky=tk.W, columnspan=1)

        btn = ttk.Button(inputFrame, text='Get Data',
                     command= getData)

        # Set the position of button on the bottom of window.
        btn.grid(column=1, row=15, sticky = tk.W)

        #create labels

        v = tk.StringVar()
        categoryLabel = tk.Label(outputFrame, textvariable=v,font=("Times New Roman", 15), width=12, anchor = tk.W)
        v.set("Category")
        categoryLabel.grid(column=1, row=0, padx=5, pady=15, sticky=tk.W, columnspan=1)

        o = tk.StringVar()
        output = tk.Label(outputFrame, textvariable=o,font=("Times New Roman", 15), width=11, anchor = tk.W)
        o.set("Value")
        output.grid(column=2, row=0, padx=5, pady=15, sticky=tk.W, columnspan=1)


        #Create Table to store JSON Data



if __name__ == "__main__":
    maingui = MainGui()
    maingui.mainloop()