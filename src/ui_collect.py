import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import re
import time
import os
import Data_Record as DR
import find_ports as fp
from utils import load_patient_names


class CollectDataPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "MainMenu.TFrame"
        self.controller = controller
        self.patient_list = []
        self.patient_var = tk.StringVar()
        self.speed_var = tk.StringVar(value="3")
        self.incline_var = tk.StringVar(value="Level")
        self.degree_var = tk.StringVar(value="0")
        self.duration_var = tk.StringVar(value="10")
        self.directory_var = tk.StringVar()
        self.countdown_seconds = 0
        self.exoskeleton_port_name = None
        self.font_style = ("Helvetica", 16)
        self.build_layout()
        self.load_patients()
        self.check_exoskeleton_connection()

    def build_layout(self):
        self.columnconfigure((0, 1, 2), weight=1, uniform="column")
        self.rowconfigure(0, weight=1)

        blue_color = "#0055A2"
        gold_color = "#C99700"
        gray_color = "#A7A8AA"
        style = ttk.Style()
        style.theme_use("clam")
        for theme, color in zip(
            ["Blue", "Gold", "Gray"], [blue_color, gold_color, gray_color]
        ):
            style.configure(
                f"{theme}.TLabelframe", background=color, font=self.font_style
            )
            style.configure(
                f"{theme}.TLabelframe.Label", background=color, font=self.font_style
            )
            style.configure(f"{theme}.TFrame", background=color)
            style.configure(f"{theme}.TLabel", background=color, font=self.font_style)
            style.configure(f"{theme}.TButton", font=self.font_style)
        style.configure("TEntry", font=self.font_style)

        # Left panel
        connect_wrapper = ttk.LabelFrame(
            self, text="Status Panel", style="Blue.TLabelframe"
        )
        connect_wrapper.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        connect_frame = ttk.Frame(connect_wrapper, style="Blue.TFrame")
        connect_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.connected_label = ttk.Label(
            connect_frame, text="Checking...", style="Blue.TLabel"
        )
        self.connected_label.pack(pady=10)
        self.retry_button = ttk.Button(
            connect_frame,
            text="Retry",
            style="Blue.TButton",
            command=self.check_exoskeleton_connection,
        )
        self.retry_button.pack(pady=10)

        # Middle panel
        middle_wrapper = ttk.LabelFrame(
            self, text="Treadmill Configuration", style="Gold.TLabelframe"
        )
        middle_wrapper.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        middle_frame = ttk.Frame(middle_wrapper, style="Gold.TFrame")
        middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(middle_frame, text="Select Patient:", style="Gold.TLabel").pack(
            anchor="w"
        )
        self.patient_dropdown = ttk.Combobox(
            middle_frame, textvariable=self.patient_var, font=self.font_style
        )
        self.patient_dropdown.pack(fill="x", pady=(0, 15))

        ttk.Label(middle_frame, text="Set Treadmill Speed:", style="Gold.TLabel").pack(
            anchor="w"
        )
        self.speed_entry = ttk.Entry(
            middle_frame, textvariable=self.speed_var, width=10, font=self.font_style
        )
        self.speed_entry.pack(anchor="w")
        ttk.Label(middle_frame, text="mph", style="Gold.TLabel").pack(anchor="w")
        self.speed_var.trace_add(
            "write", lambda *args: self.enforce_decimal_limit(self.speed_var)
        )

        ttk.Label(middle_frame, text="Elevation:", style="Gold.TLabel").pack(anchor="w")
        self.incline_dropdown = ttk.Combobox(
            middle_frame, textvariable=self.incline_var, font=self.font_style, width=15
        )
        self.incline_dropdown["values"] = ("Incline", "Level", "Decline")
        self.incline_dropdown.pack(anchor="w")
        self.incline_dropdown.bind("<<ComboboxSelected>>", self.show_or_hide_degrees)

        self.degree_container = ttk.Frame(middle_frame, style="Gold.TFrame")
        self.degree_entry = ttk.Entry(
            self.degree_container,
            textvariable=self.degree_var,
            width=10,
            font=self.font_style,
        )
        self.degree_entry.pack(side="left")
        ttk.Label(self.degree_container, text="Degrees", style="Gold.TLabel").pack(
            side="left", padx=(5, 0)
        )
        self.degree_var.trace_add(
            "write", lambda *args: self.enforce_decimal_limit(self.degree_var)
        )

        # Right panel
        right_wrapper = ttk.LabelFrame(
            self, text="Run Settings", style="Gray.TLabelframe"
        )
        right_wrapper.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        right_frame = ttk.Frame(right_wrapper, style="Gray.TFrame")
        right_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(right_frame, text="Enter Duration (sec):", style="Gray.TLabel").pack(
            anchor="w"
        )
        self.duration_entry = ttk.Entry(
            right_frame, textvariable=self.duration_var, width=10, font=self.font_style
        )
        self.duration_entry.pack(anchor="w", pady=(0, 15))

        ttk.Label(right_frame, text="Save Data To:", style="Gray.TLabel").pack(
            anchor="w"
        )
        self.directory_entry = ttk.Entry(
            right_frame, textvariable=self.directory_var, width=25, font=self.font_style
        )
        self.directory_entry.pack(anchor="w", pady=(0, 5))
        self.browse_button = ttk.Button(
            right_frame, text="Browse...", command=self.browse_directory
        )
        self.browse_button.pack(pady=(0, 10))

        self.status_icon_label = ttk.Label(
            right_frame, text="", foreground="red", style="Gray.TLabel"
        )
        self.status_icon_label.pack()
        self.status_label = ttk.Label(
            right_frame,
            text="",
            wraplength=300,
            justify="left",
            foreground="red",
            style="Gray.TLabel",
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

        self.timer_label = ttk.Label(right_frame, text="", style="Gray.TLabel")
        self.progress_bar = ttk.Progressbar(
            right_frame, mode="indeterminate", length=250
        )
        self.start_button = ttk.Button(
            right_frame,
            text="Start",
            state="disabled",
            command=self.on_start,
            style="Gray.TButton",
        )
        self.start_button.pack(pady=(0, 20))

        for var in [
            self.patient_var,
            self.speed_var,
            self.incline_var,
            self.degree_var,
            self.duration_var,
            self.directory_var,
        ]:
            var.trace_add("write", self.validate_fields)

    def browse_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.directory_var.set(folder)
            self.validate_fields()

    def enforce_decimal_limit(self, var, max_decimals=1):
        value = var.get()
        if not re.fullmatch(r"\d*(\.\d{0,%d})?" % max_decimals, value):
            var.set(value[:-1])

    def show_or_hide_degrees(self, event=None):
        if self.incline_var.get() == "Level":
            self.degree_container.pack_forget()
        else:
            self.degree_container.pack(anchor="w")
        self.validate_fields()

    def check_exoskeleton_connection(self):
        try:
            result = fp.is_exoskeleton_connected()
            if result:
                self.exoskeleton_port_name = result
                self.connected_label.config(text="Exoskeleton Connected")
                self.retry_button.config(state="disabled")
            else:
                self.exoskeleton_port_name = None
                self.connected_label.config(text="Exoskeleton Not Connected")
                self.retry_button.config(state="normal")
        except Exception as e:
            self.exoskeleton_port_name = None
            self.connected_label.config(text="Exoskeleton Error")
            self.retry_button.config(state="normal")
            messagebox.showerror("Connection Error", str(e))
        self.validate_fields()

    def validate_fields(self, *args):
        errors = []
        if not self.patient_list:
            errors.append("• No patients loaded from file")
        if not self.exoskeleton_port_name:
            errors.append("• Exoskeleton not connected")
        try:
            val = float(self.speed_var.get())
            if not (0.1 <= val <= 10):
                errors.append("• Speed must be between 0.1 and 10 mph")
        except:
            errors.append("• Speed must be a number with at most 1 decimal place")

        if self.incline_var.get() != "Level":
            try:
                deg_val = float(self.degree_var.get())
                if not (0 <= deg_val < 30):
                    errors.append("• Elevation must be less than 30 degrees")
            except:
                errors.append("• Degrees must be a number with at most 1 decimal place")

        if not self.duration_var.get():
            errors.append("• Duration is required")
        if not self.directory_var.get():
            errors.append("• Save directory is required")

        if errors:
            self.status_icon_label.config(text="⚠", foreground="red")
            self.status_label.config(text="\n".join(errors), foreground="red")
            self.start_button.config(state="disabled")
        else:
            self.status_icon_label.config(text="", foreground="green")
            self.status_label.config(text="Ready to start", foreground="green")
            self.start_button.config(state="normal")

    def update_timer(self):
        if self.countdown_seconds >= 0:
            self.timer_label.config(
                text=f"Recording... {{self.countdown_seconds}} sec remaining"
            )
            self.after(1000, self.update_timer)
            self.countdown_seconds -= 1

    def recording_finished(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.timer_label.pack_forget()
        self.start_button.pack(pady=(0, 20))
        self.status_label.config(text="Recording finished!", foreground="green")

    def on_start(self):
        self.validate_fields()
        if self.start_button["state"] == "disabled":
            messagebox.showerror("Invalid Input", self.status_label["text"])
            return

        self.check_exoskeleton_connection()
        if not self.exoskeleton_port_name:
            messagebox.showerror(
                "Exoskeleton Not Connected", "No exoskeleton port available."
            )
            return

        self.start_button.pack_forget()
        self.timer_label.pack()
        self.progress_bar.pack()
        self.progress_bar.start(10)

        name_parts = self.patient_var.get().split()
        first, middle, last = "", "", ""
        if len(name_parts) == 3:
            first, middle, last = name_parts
        elif len(name_parts) == 2:
            first, last = name_parts

        speed = self.speed_var.get()
        incline_status = self.incline_var.get()
        degrees = self.degree_var.get() if incline_status != "Level" else ""

        parts = [first]
        if middle:
            parts.append(middle)
        parts.extend([last, speed, incline_status])
        if degrees:
            parts.append(degrees)
        testname = "_".join(parts)

        total_time = int(self.duration_var.get())
        port = self.exoskeleton_port_name

        def record_task():
            try:
                DR.record_to_csv(
                    testname=os.path.join(self.directory_var.get(), testname),
                    total_time=total_time,
                    port=port,
                )
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Exoskeleton Error", f"{e}"))
            finally:
                self.after(0, self.recording_finished)

        self.countdown_seconds = total_time
        self.update_timer()
        threading.Thread(target=record_task, daemon=True).start()

    def load_patients(self):
        self.patient_list = load_patient_names()
        self.patient_dropdown["values"] = (
            self.patient_list if self.patient_list else ["No Patients Loaded"]
        )
        if self.patient_list:
            self.patient_var.set(self.patient_list[-1])
        else:
            self.patient_var.set("No Patients Loaded")
        self.validate_fields()
