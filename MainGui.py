import tkinter as tk
from tkinter import ttk
import Overrides
import Main
import datetime

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

        self.grid_propagate(False)

        # Create a frame for the canvas with non-zero row&column weights
        frame_canvas = tk.Frame(self, relief = tk.SUNKEN, borderwidth = 2,background='green',)
        frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.update_idletasks()

        # To make the output data scrollable, create a canvas that holds this frame
        outputCanvas = tk.Canvas(frame_canvas, bg="yellow")
        outputCanvas.grid(row = 0, column = 0, sticky = "news")

        #add scrollbar to canvas
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=outputCanvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        outputCanvas.configure(yscrollcommand=vsb.set)


        #Create frame for drop-down menus and button
        inputFrame = ttk.Frame(self, relief = tk.SUNKEN, borderwidth = 2)
        outputFrame = ttk.Frame(outputCanvas, relief = tk.SUNKEN, borderwidth = 2)

        inputFrame.grid(row=2, column=0, rowspan = 15, columnspan = 1, padx=10, pady=10, sticky = tk.W)
        outputFrame.grid(row = 1, column = 1, rowspan = 15, columnspan = 1, padx = 10, pady = 10, sticky = tk.W)

        #create resizable canvas window to house outputFrame
        canvas_window = outputCanvas.create_window((0, 0), window=outputFrame, anchor="nw",
                                                   # add view port frame to canvas
                                                   tags="outputFrame")

        def onFrameConfigure(event):
            '''Reset the scroll region to encompass the inner frame'''
            outputCanvas.configure(scrollregion=outputCanvas.bbox(
                "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

        def onCanvasConfigure(event):
            '''Reset the canvas window to encompass inner frame when required'''
            canvas_width = event.width
            outputCanvas.itemconfig(canvas_window,
                                    width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.

        #create bindings to accomodate changes in frame size
        outputFrame.bind("<Configure>",
                           onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        outputCanvas.bind("<Configure>",
                         onCanvasConfigure)  # bind an event whenever the size of the viewPort frame changes.

        onFrameConfigure(None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize




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

        # create summary frame

        graphFrame = ttk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        graphFrame.grid(row=0, column=1, rowspan=15, columnspan=1, padx=10, pady=10, sticky=tk.W)

        g = tk.StringVar()
        title = tk.Label(graphFrame, textvariable=g, font=("Times New Roman", 15), width=11, anchor=tk.W)
        g.set("Summary")
        title.grid(column=0, row=0, padx=5, pady=15, sticky=tk.W, columnspan=1)

        h = tk.StringVar()
        body = tk.Label(graphFrame, textvariable=h, font=("Times New Roman", 12), width=11, anchor=tk.W)
        h.set("Summary body")
        body.grid(column=0, row=1, padx=5, pady=15, sticky=tk.W, columnspan=1)

        #create submit button

        def getData():

            #First, delete all entries and labels already in the frame (but not the label in row 0)
            for widget in outputFrame.winfo_children():
                if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label) and not widget.grid_info()['row']  == 0 :
                    widget.destroy()

            Main.lowerStringVar(n)
            regionString = n.get()

            if d.get() == datetime.date.today().strftime("%Y%m%d"):
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

                if labels[x] == 'positiveIncrease':
                    positiveIncrease = self.dataDict[labels[x]]
                if labels[x] == 'inIcuCurrently':
                    inIcuCurrently = self.dataDict[labels[x]]
                if labels[x] == 'onVentilatorCurrently':
                    onVentilatorCurrently = self.dataDict[labels[x]]
                if labels[x] == 'deathIncrease':
                    deathIncrease = self.dataDict[labels[x]]
                if labels[x] == 'hospitalizedIncrease':
                    hospitalizedIncrease = self.dataDict[labels[x]]



                var = tk.StringVar()
                label = tk.Label(outputFrame, textvariable=var, width=20, anchor = tk.W)
                var.set(labels[x])
                label.grid(column=1, padx=10, row=2 * x + 1, sticky=tk.W, columnspan=1)

                out = tk.StringVar()
                output = tk.Entry(outputFrame, textvariable=out, width=22)
                out.set(self.dataDict[labels[x]])
                output.grid(column=2, padx=10, row=2 * x + 1, sticky=tk.W, columnspan=1)

            outputFrame.configure(width = 20, height = 20)

            outputCanvas.configure(yscrollcommand=vsb.set)

            outputFrame.update_idletasks()

            h.set('On ' + str(d.get())+ ", in region " + regionString +", there were " + str(positiveIncrease) + " new cases.")
            print('On ' + str(d.get())+ ", in region " + regionString +", there were " + str(positiveIncrease) + " new cases. "
                  +"Additionally, there were " + str(inIcuCurrently) + " individuals in the ICU on this day, and " + str(onVentilatorCurrently)
                  + " individuals on a ventilator. \n Furthermore, deaths increased by " + str(deathIncrease) + ", and hospitalizations by "
                  + str(hospitalizedIncrease)+"."
                  )

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


        #create graphing input box
        graphInputFrame = ttk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        graphInputFrame.grid(row=2, column=1, rowspan=15, columnspan=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(graphInputFrame, text="Select the Region :",
                  font=("Times New Roman", 10), width=20).grid(column=0,
                                                               row=5, padx=10, pady=8, sticky=tk.W)

        ttk.Label(graphInputFrame, text="Select the date :",
                  font=("Times New Roman", 10), width=20).grid(column=0,
                                                               row=8, padx=10, pady=8, sticky=tk.W)
        ttk.Label(graphInputFrame, text="Graph Categories :",
                  font=("Times New Roman", 10), width=20).grid(column=0,
                                                               row=11, padx=10, pady=8, sticky=tk.W)

        ttk.Label(graphInputFrame, text="Rolling Average (Days):",
                  font=("Times New Roman", 10), width=23).grid(column=0,
                                                               row=14, padx=10, pady=8, sticky=tk.W)

        # make region dropdown menu
        v = tk.StringVar()
        regionGraph = ttk.Combobox(graphInputFrame, width=20, textvariable=v)

        # Adding combobox drop down list
        regionGraph['values'] = ("US", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY")

        regionGraph.grid(column=1, row=5, sticky=tk.W)
        # set default to first region
        regionGraph.current(0)

        #Add graph category drop down list
        k = tk.StringVar()
        categories = ttk.Combobox(graphInputFrame, width=20, textvariable=k)

        #create set that stores selected categories; make it an instance variable so it can be changed beyond where it is used here
        self.selectedCats = {}
        self.selectedCats = set()

        # create function that creates new stringvar for a multiselect type tool
        def addNewItem(event):
            self.selectedCats.add(k.get())
            print(self.selectedCats)

            #regenerate string from set every time to avoid duplicates
            catString = ""
            for elem in self.selectedCats:
                catString += elem + ", "
            k.set(catString)

        #bind addNewItem method to selection of category
        categories.bind("<<ComboboxSelected>>", addNewItem)



        # Adding combobox drop down list
        categories['values'] = ("positive","negative","pending","hospitalizedCurrently",
                              "hospitalizedCumulative","inIcuCurrently","inIcuCumulative",
                              "onVentilatorCurrently","totalTestResults","deathIncrease",
                              "hospitalizedIncrease","negativeIncrease","positiveIncrease",
                                                                        "totalTestResultsIncrease"
                              )

        categories.grid(column=1, row=11, sticky=tk.W)


        # create cal
        c = tk.StringVar()

        cal = Overrides.CustomDateEntry(graphInputFrame, textvariable=c, date_pattern='yyyymmdd', width=20,
                                        bg="darkblue",
                                        fg="white", year=2020)

        cal.grid(column=1, row=8, sticky=tk.W)


        #Add rolling average Entry
        y = tk.IntVar()

        averageEntry = ttk.Entry(graphInputFrame, width=23, textvariable=y)

        averageEntry.grid(column=1, row=14, sticky=tk.W)


        def getGraph():

            graphCategories = list(self.selectedCats)
            if c.get() == datetime.date.today().strftime("%Y%m%d"):
                #make sure that when graphing the day is always one day behind
                today = datetime.date.today()
                diff = datetime.timedelta(days = 1)

                gdate = today - diff
                graphDate = gdate.strftime("%Y%m%d")
            else:
                graphDate = c.get()

            if(v.get() == 'US'):
                graphRegion = 'us'
            else:
                graphRegion = v.get()

            rollingAverageInt = y.get()

            Main.graphCovidData(graphCategories, int(graphDate), graphRegion, rollingAverageInt)

        btn = ttk.Button(graphInputFrame, text='Get Graph',
                         command=getGraph)

        # Set the position of button on the bottom of window.
        btn.grid(column=1, row=15, sticky=tk.W)

        def resetGraphCats():
            self.selectedCats = {}
            self.selectedCats = set()
            k.set('')

        resetbtn = ttk.Button(graphInputFrame, text='Reset Graph Categories',
                         command=resetGraphCats)

        # Set the position of button on the bottom of window.
        resetbtn.grid(column=0, row=15, padx=10,sticky=tk.W)

if __name__ == "__main__":
    maingui = MainGui()
    maingui.mainloop()