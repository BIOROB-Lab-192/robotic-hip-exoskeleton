# Complete Exoskeleton Treadmill Data Collection App

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import pandas as pd
from datetime import datetime
import threading
import time
import find_ports as fp
import Data_Record as DR

DATA_DIR = "data"
INFO_FILE = os.path.join(DATA_DIR, "patient_info.csv")
DATA_FILE = os.path.join(DATA_DIR, "patient_data.csv")


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(INFO_FILE):
        pd.DataFrame(
            columns=[
                "Patient_ID",
                "First Name",
                "Middle Name",
                "Last Name",
                "Phone",
                "Email",
            ]
        ).to_excel(INFO_FILE, index=False)
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(
            columns=[
                "Patient_ID",
                "Height_cm",
                "weight_kg",
                "gender",
                "dob",
                "date_enrolled",
                "mobility_status",
                "notes",
            ]
        ).to_excel(DATA_FILE, index=False)


def get_next_patient_id():
    try:
        df = pd.read_excel(INFO_FILE)
        return int(df["Patient_ID"].max()) + 1 if not df.empty else 1
    except:
        return 1


def load_patient_names():
    try:
        df = pd.read_excel(INFO_FILE)
        names = []
        for _, row in df.iterrows():
            first = str(row["First Name"]).strip().title()
            middle = (
                str(row["Middle Name"]).strip()
                if not pd.isna(row["Middle Name"])
                else ""
            )
            last = str(row["Last Name"]).strip().title()
            if not first or not last:
                continue
            name = f"{first} {middle[0] + '.' if middle else ''} {last}"
            names.append(name)
        return names
    except:
        return []


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Exoskeleton Treadmill Data Collection App")
        self.geometry("1000x600")
        self.frames = {}

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (MainMenu, ViewPatientsPage, AddPatientPage, CollectDataPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "ViewPatientsPage":
            frame.load_data()
        if page_name == "CollectDataPage":
            frame.load_patients()
        frame.tkraise()


class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=40)

        ttk.Label(self, text="Main Menu", font=("Helvetica", 24)).pack(pady=20)
        ttk.Button(
            self,
            text="View Patients",
            command=lambda: controller.show_frame("ViewPatientsPage"),
        ).pack(pady=10, ipadx=20, ipady=10, fill="x")
        ttk.Button(
            self,
            text="Add New Patient",
            command=lambda: controller.show_frame("AddPatientPage"),
        ).pack(pady=10, ipadx=20, ipady=10, fill="x")
        ttk.Button(
            self,
            text="Collect Data",
            command=lambda: controller.show_frame("CollectDataPage"),
        ).pack(pady=10, ipadx=20, ipady=10, fill="x")


class ViewPatientsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="All Patients", font=("Helvetica", 20)).pack(pady=10)
        self.tree = ttk.Treeview(self, columns=(), show="headings")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("MainMenu")
        ).pack(pady=10)

    def load_data(self):
        try:
            info_df = pd.read_excel(INFO_FILE)
            data_df = pd.read_excel(DATA_FILE)
            merged_df = pd.merge(info_df, data_df, on="Patient_ID", how="outer")
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(merged_df.columns)
            for col in merged_df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120)
            for _, row in merged_df.iterrows():
                self.tree.insert("", "end", values=list(row.fillna("")))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient data:\n{e}")


class AddPatientPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Add New Patient", font=("Helvetica", 20)).pack(pady=10)
        form = ttk.Frame(self)
        form.pack(pady=10)
        self.entries = {}
        fields_info = [
            ("First Name", tk.StringVar()),
            ("Middle Name", tk.StringVar()),
            ("Last Name", tk.StringVar()),
            ("Phone", tk.StringVar()),
            ("Email", tk.StringVar()),
            ("Height_cm", tk.StringVar()),
            ("weight_kg", tk.StringVar()),
            ("gender", tk.StringVar()),
            ("dob (YYYY-MM-DD)", tk.StringVar()),
            ("mobility_status", tk.StringVar()),
            ("notes", tk.StringVar()),
        ]
        for i, (label_text, var) in enumerate(fields_info):
            ttk.Label(form, text=label_text).grid(
                row=i, column=0, sticky="e", padx=5, pady=2
            )
            entry = ttk.Entry(form, textvariable=var, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[label_text] = var
        ttk.Button(self, text="Submit", command=self.submit).pack(pady=10)
        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("MainMenu")
        ).pack()

    def submit(self):
        pid = get_next_patient_id()
        info_data = {
            "Patient_ID": pid,
            "First Name": self.entries["First Name"].get(),
            "Middle Name": self.entries["Middle Name"].get(),
            "Last Name": self.entries["Last Name"].get(),
            "Phone": self.entries["Phone"].get(),
            "Email": self.entries["Email"].get(),
        }
        data_data = {
            "Patient_ID": pid,
            "Height_cm": self.entries["Height_cm"].get(),
            "weight_kg": self.entries["weight_kg"].get(),
            "gender": self.entries["gender"].get(),
            "dob": self.entries["dob (YYYY-MM-DD)"].get(),
            "date_enrolled": datetime.now().strftime("%Y-%m-%d"),
            "mobility_status": self.entries["mobility_status"].get(),
            "notes": self.entries["notes"].get(),
        }
        try:
            info_df = pd.read_excel(INFO_FILE)
            data_df = pd.read_excel(DATA_FILE)
            info_df = pd.concat([info_df, pd.DataFrame([info_data])], ignore_index=True)
            data_df = pd.concat([data_df, pd.DataFrame([data_data])], ignore_index=True)
            info_df.to_excel(INFO_FILE, index=False)
            data_df.to_excel(DATA_FILE, index=False)
            messagebox.showinfo("Success", f"Patient {pid} added successfully!")
            self.controller.show_frame("MainMenu")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save patient:\n{e}")


class CollectDataPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.patient_list = []
        self.exoskeleton_port_name = None

        ttk.Label(self, text="Treadmill Data Collection", font=("Helvetica", 20)).pack(
            pady=10
        )

        self.content = ttk.Frame(self)
        self.content.pack(pady=10)

        self.status_var = tk.StringVar()
        self.timer_label = ttk.Label(
            self.content, textvariable=self.status_var, foreground="green"
        )
        self.timer_label.pack()

        # Form
        self.patient_var = tk.StringVar()
        ttk.Label(self.content, text="Select Patient:").pack(anchor="w")
        self.patient_dropdown = ttk.Combobox(
            self.content, textvariable=self.patient_var, state="readonly"
        )
        self.patient_dropdown.pack(fill="x", pady=5)

        self.speed_var = tk.StringVar(value="1.0")
        ttk.Label(self.content, text="Speed (mph):").pack(anchor="w")
        self.speed_entry = ttk.Entry(self.content, textvariable=self.speed_var)
        self.speed_entry.pack(fill="x", pady=5)

        self.incline_var = tk.StringVar(value="Level")
        ttk.Label(self.content, text="Incline Type:").pack(anchor="w")
        self.incline_dropdown = ttk.Combobox(
            self.content,
            textvariable=self.incline_var,
            values=["Incline", "Level", "Decline"],
            state="readonly",
        )
        self.incline_dropdown.pack(fill="x", pady=5)

        self.degrees_var = tk.StringVar(value="0")
        ttk.Label(self.content, text="Incline Degrees:").pack(anchor="w")
        self.degrees_entry = ttk.Entry(self.content, textvariable=self.degrees_var)
        self.degrees_entry.pack(fill="x", pady=5)

        self.duration_var = tk.StringVar(value="10")
        ttk.Label(self.content, text="Duration (sec):").pack(anchor="w")
        self.duration_entry = ttk.Entry(self.content, textvariable=self.duration_var)
        self.duration_entry.pack(fill="x", pady=5)

        self.directory_var = tk.StringVar()
        ttk.Label(self.content, text="Save Directory:").pack(anchor="w")
        self.dir_entry = ttk.Entry(self.content, textvariable=self.directory_var)
        self.dir_entry.pack(fill="x", pady=5)
        ttk.Button(self.content, text="Browse", command=self.browse_directory).pack(
            pady=5
        )

        self.start_btn = ttk.Button(
            self.content, text="Start Test", command=self.start_test
        )
        self.start_btn.pack(pady=10)

        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("MainMenu")
        ).pack(pady=10)

        self.progress = ttk.Progressbar(self.content, mode="indeterminate")

    def load_patients(self):
        self.patient_list = load_patient_names()
        self.patient_dropdown["values"] = self.patient_list
        if self.patient_list:
            self.patient_var.set(self.patient_list[-1])

    def browse_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.directory_var.set(folder)

    def check_exoskeleton(self):
        try:
            result = fp.is_exoskeleton_connected()
            if result:
                self.exoskeleton_port_name = result
                return True
            else:
                self.exoskeleton_port_name = None
                return False
        except Exception as e:
            self.status_var.set(f"Exoskeleton Error: {e}")
            return False

    def start_test(self):
        if not self.patient_var.get():
            self.status_var.set("Select a patient.")
            return
        if (
            not self.speed_var.get().replace(".", "", 1).isdigit()
            or float(self.speed_var.get()) > 10
        ):
            self.status_var.set("Speed must be a number ≤ 10.")
            return
        if self.incline_var.get() != "Level":
            if (
                not self.degrees_var.get().replace(".", "", 1).isdigit()
                or float(self.degrees_var.get()) >= 30
            ):
                self.status_var.set("Incline degrees must be < 30.")
                return
        if not self.duration_var.get().isdigit():
            self.status_var.set("Enter valid duration.")
            return
        if not os.path.isdir(self.directory_var.get()):
            self.status_var.set("Invalid directory.")
            return
        if not self.check_exoskeleton():
            self.status_var.set("Exoskeleton not connected.")
            return

        # Start
        self.status_var.set("Recording...")
        self.progress.pack(pady=10)
        self.progress.start()

        name_parts = self.patient_var.get().split()
        testname = "_".join(name_parts + [self.speed_var.get(), self.incline_var.get()])
        if self.incline_var.get() != "Level":
            testname += "_" + self.degrees_var.get()

        duration = int(self.duration_var.get())
        port = self.exoskeleton_port_name

        threading.Thread(
            target=self.run_recording, args=(testname, duration, port), daemon=True
        ).start()

    def run_recording(self, testname, duration, port):
        try:
            DR.record_to_csv(testname, duration, port)
            self.status_var.set("Test complete.")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()


if __name__ == "__main__":
    ensure_data_files()
    app = App()
    app.mainloop()
