
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import os
from utils import INFO_FILE, DATA_FILE, get_next_patient_id

class AddPatientPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Add New Patient", font=("Helvetica", 20)).pack(pady=10)
        form = ttk.Frame(self)
        form.pack(pady=10)

        self.entries = {}
        row = 0

        def add_row(label, is_optional=False):
            nonlocal row
            label_text = f"{label} (optional)" if is_optional else label
            ttk.Label(form, text=label_text).grid(row=row, column=0, sticky="e", padx=(5, 5), pady=2)
            var = tk.StringVar()
            entry = ttk.Entry(form, textvariable=var, width=30)
            entry.grid(row=row, column=1, sticky="w", pady=2)
            self.entries[label] = var
            row += 1

        add_row("First Name")
        add_row("Middle Name", is_optional=True)
        add_row("Last Name")
        add_row("Phone", is_optional=True)
        add_row("Email", is_optional=True)
        add_row("Height (cm)")
        add_row("Weight (kg)")

        ttk.Label(form, text="Gender").grid(row=row, column=0, sticky="e", padx=(5, 5), pady=2)
        self.gender_var = tk.StringVar()
        gender_menu = ttk.Combobox(form, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly", width=28)
        gender_menu.grid(row=row, column=1, sticky="w", pady=2)
        self.entries["Gender"] = self.gender_var
        row += 1

        ttk.Label(form, text="Date of Birth").grid(row=row, column=0, sticky="e", padx=(5, 5), pady=2)
        dob_frame = ttk.Frame(form)
        dob_frame.grid(row=row, column=1, sticky="w", pady=2)

        self.dob_month = tk.StringVar()
        self.dob_day = tk.StringVar()
        self.dob_year = tk.StringVar()

        self.month_box = ttk.Combobox(dob_frame, textvariable=self.dob_month, values=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], state="readonly", width=6)
        self.day_box = ttk.Combobox(dob_frame, textvariable=self.dob_day, state="readonly", width=4)
        self.year_box = ttk.Combobox(dob_frame, textvariable=self.dob_year, values=[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900], state="readonly", width=6)

        self.month_box.pack(side="left")
        self.day_box.pack(side="left", padx=5)
        self.year_box.pack(side="left")

        self.dob_month.trace_add("write", lambda *args: self.update_days())
        self.dob_year.trace_add("write", lambda *args: self.update_days())
        row += 1

        ttk.Label(form, text="Mobility Status").grid(row=row, column=0, sticky="e", padx=(5, 5), pady=2)
        self.mobility_var = tk.StringVar()
        mobility_options = ["Normal", "Cerebral Palsy", "Stroke", "Parkinson's", "Other"]
        mobility_menu = ttk.Combobox(form, textvariable=self.mobility_var, values=mobility_options, state="readonly", width=28)
        mobility_menu.grid(row=row, column=1, sticky="w", pady=2)
        self.entries["Mobility Status"] = self.mobility_var
        row += 1

        ttk.Label(form, text="Notes").grid(row=row, column=0, sticky="ne", padx=(5, 5), pady=2)
        self.notes_text = tk.Text(form, width=40, height=4)
        self.notes_text.grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Button(self, text="Submit", command=self.submit).pack(pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenu")).pack()

    def update_days(self):
        month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = self.dob_month.get()
        year = self.dob_year.get()
        if not month or not year:
            return

        month_idx = {abbr: i for i, abbr in enumerate(month_abbr, start=1)}.get(month, 1)
        year = int(year)
        days_in_month = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                         31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        valid_days = list(range(1, days_in_month[month_idx - 1] + 1))
        self.day_box["values"] = valid_days
        if self.dob_day.get() and int(self.dob_day.get()) not in valid_days:
            self.dob_day.set("")

    def submit(self):
        required = ["First Name", "Last Name", "Height (cm)", "Weight (kg)", "Gender", "Mobility Status"]
        for field in required:
            if not self.entries[field].get().strip():
                messagebox.showerror("Missing Field", f"Please fill in the '{field}' field.")
                return
        if not (self.dob_day.get() and self.dob_month.get() and self.dob_year.get()):
            messagebox.showerror("Missing Field", "Please complete the Date of Birth.")
            return

        month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_idx = {abbr: i for i, abbr in enumerate(month_abbr, start=1)}.get(self.dob_month.get(), 1)
        dob = f"{self.dob_year.get()}-{str(month_idx).zfill(2)}-{self.dob_day.get().zfill(2)}"
        pid = get_next_patient_id()

        info_data = {
            "Patient_ID": pid,
            "First Name": self.entries["First Name"].get(),
            "Middle Name": self.entries["Middle Name"].get(),
            "Last Name": self.entries["Last Name"].get(),
            "Phone": self.entries["Phone"].get(),
            "Email": self.entries["Email"].get()
        }
        data_data = {
            "Patient_ID": pid,
            "Height_cm": self.entries["Height (cm)"].get(),
            "weight_kg": self.entries["Weight (kg)"].get(),
            "gender": self.entries["Gender"].get(),
            "dob": dob,
            "date_enrolled": datetime.now().strftime("%Y-%m-%d"),
            "mobility_status": self.entries["Mobility Status"].get(),
            "notes": self.notes_text.get("1.0", "end").strip()
        }

        try:
            info_df = pd.read_csv(INFO_FILE)
            data_df = pd.read_csv(DATA_FILE)
            info_df = pd.concat([info_df, pd.DataFrame([info_data])], ignore_index=True)
            data_df = pd.concat([data_df, pd.DataFrame([data_data])], ignore_index=True)
            info_df.to_csv(INFO_FILE, index=False)
            data_df.to_csv(DATA_FILE, index=False)
            messagebox.showinfo("Success", f"Patient {pid} added successfully!")
            self.controller.show_frame("MainMenu")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save patient:\n{e}")
