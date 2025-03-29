import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from utils import load_patient_dataframe, save_patient_dataframe

class ViewPatientsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self["style"] = "Blue.TFrame"

        style = ttk.Style()
        style.theme_use("clam")
        self.font_style = ("Helvetica", 14)
        style.configure("Blue.TFrame", background="#0055A2")
        style.configure("Header.TLabel", background="#0055A2", foreground="white", font=("Helvetica", 20, "bold"))
        style.configure("Gray.TButton", background="#A7A8AA", font=self.font_style, padding=10)
        style.map("Gray.TButton", background=[("active", "#8e8f90")])

        ttk.Label(self, text="All Patients", style="Header.TLabel").pack(pady=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "First", "Middle", "Last", "Phone", "Email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self, style="Blue.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Delete Selected", style="Gray.TButton", command=self.delete_selected).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Back", style="Gray.TButton", command=lambda: controller.show_frame("MainMenu")).pack(side="left", padx=10)

        self.load_data()

    def load_data(self):
        df = load_patient_dataframe()
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row.get("Patient_ID", ""),
                row.get("First Name", ""),
                row.get("Middle Name", ""),
                row.get("Last Name", ""),
                row.get("Phone", ""),
                row.get("email", "")
            ))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a patient to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected patient?")
        if not confirm:
            return

        selected_values = self.tree.item(selected_item)["values"]
        patient_id = selected_values[0]

        df = load_patient_dataframe()
        df = df[df["Patient_ID"] != patient_id]
        save_patient_dataframe(df)

        self.tree.delete(selected_item)