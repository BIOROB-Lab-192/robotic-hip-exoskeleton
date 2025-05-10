import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import date
from utils import get_next_patient_id, load_patient_dataframe, update_patient_dataframe
import calendar


class AddPatientPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.font_style = ("Helvetica", 14)

        self.configure(style="Blue.TFrame")
        ttk.Label(
            self, text="Add New Patient", font=("Helvetica", 20), style="Blue.TLabel"
        ).pack(pady=10)
        form = ttk.Frame(self, style="Blue.TFrame")
        form.pack(pady=10)

        self.entries = {}

        fields = [
            ("First Name*", "first_name"),
            ("Middle Name (optional)", "middle_name"),
            ("Last Name*", "last_name"),
            ("Phone (optional)", "phone"),
            ("Email (optional)", "email"),
            ("Height (cm)*", "height"),
            ("Weight (kg)*", "weight"),
        ]

        for i, (label_text, key) in enumerate(fields):
            label = ttk.Label(form, text=label_text, style="Blue.TLabel")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = ttk.Entry(form, font=self.font_style)
            entry.grid(row=i, column=1, pady=2, sticky="w")
            self.entries[key] = entry

        # Gender Dropdown
        ttk.Label(form, text="Gender*", style="Blue.TLabel").grid(
            row=len(fields), column=0, sticky="e", padx=5
        )
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(
            form,
            textvariable=self.gender_var,
            values=["Male", "Female", "Other"],
            font=self.font_style,
        )
        gender_combo.grid(row=len(fields), column=1, sticky="w")
        gender_combo.current(0)

        # DOB dropdowns
        ttk.Label(form, text="Date of Birth*", style="Blue.TLabel").grid(
            row=len(fields) + 1, column=0, sticky="e", padx=5
        )
        dob_frame = ttk.Frame(form, style="Blue.TFrame")
        dob_frame.grid(row=len(fields) + 1, column=1, sticky="w")

        self.dob_year_var = tk.StringVar()
        self.dob_month_var = tk.StringVar()
        self.dob_day_var = tk.StringVar()

        self.years = [str(y) for y in range(date.today().year, 1900, -1)]
        self.months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        self.days = [str(d) for d in range(1, 32)]

        ttk.Combobox(
            dob_frame, textvariable=self.dob_year_var, values=self.years, width=5
        ).pack(side="left")
        ttk.Combobox(
            dob_frame, textvariable=self.dob_month_var, values=self.months, width=5
        ).pack(side="left", padx=2)
        self.day_dropdown = ttk.Combobox(
            dob_frame, textvariable=self.dob_day_var, values=self.days, width=3
        )
        self.day_dropdown.pack(side="left")

        self.dob_year_var.trace_add("write", self.update_day_options)
        self.dob_month_var.trace_add("write", self.update_day_options)

        # Mobility
        ttk.Label(form, text="Mobility Status*", style="Blue.TLabel").grid(
            row=len(fields) + 2, column=0, sticky="e", padx=5
        )
        self.mobility_var = tk.StringVar()
        ttk.Combobox(
            form,
            textvariable=self.mobility_var,
            values=["Normal", "Cerebral Palsy", "Stroke", "Other"],
            font=self.font_style,
        ).grid(row=len(fields) + 2, column=1, sticky="w")

        # Notes
        ttk.Label(form, text="Notes (optional)", style="Blue.TLabel").grid(
            row=len(fields) + 3, column=0, sticky="ne", padx=5
        )
        self.notes_text = tk.Text(form, height=3, width=30)
        self.notes_text.grid(row=len(fields) + 3, column=1, sticky="w")

        ttk.Button(self, text="Save Patient", command=self.save_patient).pack(pady=15)
        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("MainMenu")
        ).pack(pady=10)

    def update_day_options(self, *args):
        try:
            year = int(self.dob_year_var.get())
            month = self.months.index(self.dob_month_var.get()) + 1
            days_in_month = calendar.monthrange(year, month)[1]
        except Exception:
            days_in_month = 31
        self.day_dropdown["values"] = [str(i) for i in range(1, days_in_month + 1)]
        if self.dob_day_var.get() not in self.day_dropdown["values"]:
            self.dob_day_var.set("")

    def save_patient(self):
        info_df, data_df = load_patient_dataframe()
        pid = str(get_next_patient_id())

        first = self.entries["first_name"].get().strip()
        last = self.entries["last_name"].get().strip()
        height = self.entries["height"].get().strip()
        weight = self.entries["weight"].get().strip()

        if not all(
            [
                first,
                last,
                height,
                weight,
                self.gender_var.get(),
                self.dob_year_var.get(),
                self.dob_month_var.get(),
                self.dob_day_var.get(),
                self.mobility_var.get(),
            ]
        ):
            messagebox.showerror(
                "Missing Fields", "Please fill out all required fields."
            )
            return

        phone = self.entries["phone"].get().strip()
        email = self.entries["email"].get().strip()
        if phone and not phone.isdigit():
            messagebox.showerror("Invalid Phone", "Phone number must be numeric.")
            return
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        info_df.loc[len(info_df)] = {
            "Patient_ID": pid,
            "First Name": first,
            "Middle Name": self.entries["middle_name"].get().strip(),
            "Last Name": last,
            "Phone": int(phone) if phone else "",
            "Email": email,
        }

        dob = f"{self.dob_day_var.get()}-{self.dob_month_var.get()}-{self.dob_year_var.get()}"
        data_df.loc[len(data_df)] = {
            "Patient_ID": pid,
            "Height_cm": height,
            "weight_kg": weight,
            "gender": self.gender_var.get(),
            "dob": dob,
            "date_enrolled": str(date.today()),
            "mobility_status": self.mobility_var.get(),
            "notes": self.notes_text.get("1.0", "end").strip(),
        }

        update_patient_dataframe(info_df, data_df)
        messagebox.showinfo("Success", "Patient added successfully.")

        # Clear fields
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.gender_var.set("")
        self.dob_year_var.set("")
        self.dob_month_var.set("")
        self.dob_day_var.set("")
        self.mobility_var.set("")
        self.notes_text.delete("1.0", "end")

        self.controller.show_frame("MainMenu")
