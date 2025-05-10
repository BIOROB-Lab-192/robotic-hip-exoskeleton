import tkinter as tk
from tkinter import ttk


class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        style = ttk.Style()
        style.theme_use("clam")
        self.font_style = ("Helvetica", 18)

        # Define colors
        style.configure("MainMenu.TFrame", background="#0055A2")
        style.configure(
            "Gray.TButton", background="#A7A8AA", font=self.font_style, padding=10
        )
        style.map("Gray.TButton", background=[("active", "#8e8f90")])
        style.configure(
            "MainMenu.TLabel",
            background="#0055A2",
            foreground="white",
            font=("Helvetica", 24, "bold"),
        )

        self["style"] = "MainMenu.TFrame"

        # Heading
        ttk.Label(self, text="Main Menu", style="MainMenu.TLabel").pack(pady=20)

        # Buttons
        ttk.Button(
            self,
            text="View Patients",
            style="Gray.TButton",
            command=lambda: controller.show_frame("ViewPatientsPage"),
        ).pack(pady=10, ipadx=20, ipady=10, fill="x")

        ttk.Button(
            self,
            text="Add New Patient",
            style="Gray.TButton",
            command=lambda: controller.show_frame("AddPatientPage"),
        ).pack(pady=10, ipadx=20, ipady=10, fill="x")

        ttk.Button(
            self,
            text="Collect Data",
            style="Gray.TButton",
            command=lambda: controller.show_frame("CollectDataPage"),
        ).pack(pady=10, ipadx=20, ipady=10, fill="x")
