import tkinter as tk
from tkinter import ttk
from ui_main_menu import MainMenu
from patient_add import AddPatientPage
from ui_collect import CollectDataPage
from patient_view import ViewPatientsPage
from patient_edit import EditPatientPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Exoskeleton Treadmill Data Collection App")
        self.geometry("1000x600")
        self.configure(bg="#0055A2")  # SJSU blue background

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container

        self.frames = {}
        for F in (MainMenu, AddPatientPage, CollectDataPage, ViewPatientsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "load_patients"):
            frame.load_patients()
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
