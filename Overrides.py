import platform
import re
import tkcalendar as tkcal
from tkinter import ttk
import tkinter as tk

#override parse_date method in _calendar.py to fit api grab date format.
#This requires also overriding the DateEntry, as parse_date is called from this class.

class CustomCalendar(tkcal.Calendar):

    """

    Custom Calendar Class
    """

    def parse_date(self, date):
        """Parse string date in the locale format and return the corresponding datetime.date."""
        date_format = self._properties['date_pattern'].lower()
        year_idx = date_format.index('y')
        month_idx = date_format.index('m')
        day_idx = date_format.index('d')

        indexes = [(year_idx, 'Y'), (month_idx, 'M'), (day_idx, 'D')]
        indexes.sort()

        numbers = re.findall(r'(\d+)', date)

        if len(numbers) == 1:

            for x in range(len(indexes)):
                if(indexes[x][1] == 'Y'):
                    yearSubstr = date[indexes[x][0]:indexes[x][0] + 4]
                if(indexes[x][1] == 'M'):
                    monthSubstr = date[indexes[x][0]:indexes[x][0] + 2]
                if (indexes[x][1] == 'D'):
                    daySubstr = date[indexes[x][0]:indexes[x][0] + 2]

            year = int(yearSubstr)
            month = int(monthSubstr)
            day = int(daySubstr)
            if month > 12:
                month, day = day, month
            return self.date(year, month, day)

        else:
            indexes = dict([(item[1], idx) for idx, item in enumerate(indexes)])

            year = numbers[indexes['Y']]
            if len(year) == 2:
                year = 2000 + int(year)
            else:
                year = int(year)
            month = int(numbers[indexes['M']])
            day = int(numbers[indexes['D']])
            if month > 12:
                month, day = day, month
            return self.date(year, month, day)

class CustomDateEntry(tkcal.DateEntry):
    def __init__(self, master=None, **kw):
        """
        Create an entry with a drop-down calendar to select a date.

        When the entry looses focus, if the user input is not a valid date,
        the entry content is reset to the last valid date.

        Keyword Options
        ---------------

        usual ttk.Entry options and Calendar options.
        The Calendar option 'cursor' has been renamed
        'calendar_cursor' to avoid name clashes with the
        corresponding ttk.Entry option.

        Virtual event
        -------------

        A ``<<DateEntrySelected>>`` event is generated each time
        the user selects a date.

        """
        # sort keywords between entry options and calendar options
        kw['selectmode'] = 'day'
        entry_kw = {}

        style = kw.pop('style', 'DateEntry')

        for key in self.entry_kw:
            entry_kw[key] = kw.pop(key, self.entry_kw[key])
        entry_kw['font'] = kw.get('font', None)
        self._cursor = entry_kw['cursor']  # entry cursor
        kw['cursor'] = kw.pop('calendar_cursor', None)

        ttk.Entry.__init__(self, master, **entry_kw)

        self._determine_downarrow_name_after_id = ''

        # drop-down calendar
        self._top_cal = tk.Toplevel(self)
        self._top_cal.withdraw()
        if platform == "linux":
            self._top_cal.attributes('-type', 'DROPDOWN_MENU')
        self._top_cal.overrideredirect(True)
        self._calendar = CustomCalendar(self._top_cal, **kw)
        self._calendar.pack()

        # locale date parsing / formatting
        self.format_date = self._calendar.format_date
        self.parse_date = self._calendar.parse_date

        # style
        self._theme_name = ''   # to detect theme changes
        self.style = ttk.Style(self)
        self._setup_style()
        self.configure(style=style)

        # add validation to Entry so that only dates in the locale's format
        # are accepted
        validatecmd = self.register(self._validate_date)
        self.configure(validate='focusout',
                       validatecommand=validatecmd)

        # initially selected date
        self._date = self._calendar.selection_get()
        if self._date is None:
            today = self._calendar.date.today()
            year = kw.get('year', today.year)
            month = kw.get('month', today.month)
            day = kw.get('day', today.day)
            try:
                self._date = self._calendar.date(year, month, day)
            except ValueError:
                self._date = today
        self._set_text(self.format_date(self._date))

        # --- bindings
        # reconfigure style if theme changed
        self.bind('<<ThemeChanged>>',
                  lambda e: self.after(10, self._on_theme_change))
        # determine new downarrow button bbox
        self.bind('<Configure>', self._determine_downarrow_name)
        self.bind('<Map>', self._determine_downarrow_name)
        # handle appearence to make the entry behave like a Combobox but with
        # a drop-down calendar instead of a drop-down list
        self.bind('<Leave>', lambda e: self.state(['!active']))
        self.bind('<Motion>', self._on_motion)
        self.bind('<ButtonPress-1>', self._on_b1_press)
        # update entry content when date is selected in the Calendar
        self._calendar.bind('<<CalendarSelected>>', self._select)
        # hide calendar if it looses focus
        self._calendar.bind('<FocusOut>', self._on_focus_out_cal)