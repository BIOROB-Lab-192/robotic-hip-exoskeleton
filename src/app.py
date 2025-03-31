import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import pandas as pd
import os
import threading
import time
import find_ports as fp
import Data_Record as DR  # Recording method


exoskeleton_port_name = None
countdown_seconds = 0


def load_patient_names():
    filename = "data/patient_info.csv"
    if not os.path.exists(filename):
        return []

    try:
        df = pd.read_excel(filename)
        df.columns = df.columns.str.strip()
        names = []
        for _, row in df.iterrows():
            first = (
                str(row["First Name"]).strip().title()
                if not pd.isna(row["First Name"])
                else ""
            )
            middle = (
                str(row["Middle Name"]).strip()
                if not pd.isna(row["Middle Name"])
                else ""
            )
            last = (
                str(row["Last Name"]).strip().title()
                if not pd.isna(row["Last Name"])
                else ""
            )
            if not first or not last:
                continue
            full_name = f"{first} {middle[0] + '.' if middle else ''} {last}".strip()
            names.append(full_name)
        return names
    except Exception as e:
        print("Error loading patient_info.csv:", e)
        return []


# ───────────── Validation Helpers ─────────────
def is_valid_decimal(value, max_decimals=1, min_value=0.1, max_value=10.0):
    try:
        float_val = float(value)
        if float_val < min_value or float_val > max_value:
            return False
        return True
    except ValueError:
        return False


def enforce_decimal_limit(var, max_decimals=1):
    value = var.get()
    if not re.fullmatch(r"\d*(\.\d{0,%d})?" % max_decimals, value):
        var.set(value[:-1])


# ───────────── Field Validation ─────────────
def validate_fields(*args):
    errors = []

    if not patient_list:
        errors.append("• No patients loaded from file")
    if not exoskeleton_port_name:
        errors.append("• Exoskeleton not connected")

    # SPEED
    speed = speed_var.get()
    if not re.fullmatch(r"\d*(\.\d{0,1})?", speed):
        errors.append("• Speed must be a number with at most 1 decimal place")
    else:
        try:
            val = float(speed)
            if not (0.1 <= val <= 10):
                errors.append("• Speed must be between 0.1 and 10 mph")
        except:
            errors.append("• Speed input is not a valid number")

    # DEGREES
    if incline_var.get() != "Level":
        deg = degree_var.get()
        if not re.fullmatch(r"\d*(\.\d{0,1})?", deg):
            errors.append("• Degrees must be a number with at most 1 decimal place")
        else:
            try:
                deg_val = float(deg)
                if not (0 <= deg_val < 30):
                    errors.append("• Elevation must be less than 30 degrees")
            except:
                errors.append("• Degrees input is not a valid number")

    if not duration_var.get():
        errors.append("• Duration is required")
    if not directory_var.get():
        errors.append("• Save directory is required")

    if errors:
        status_icon_label.config(text="⚠", foreground="red")
        status_label.config(text="\n".join(errors), foreground="red")
        start_button.config(state="disabled")
    else:
        status_icon_label.config(text="", foreground="green")
        status_label.config(text="Ready to start", foreground="green")
        start_button.config(state="normal")


# ───────────── UI Handlers ─────────────
def browse_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        directory_var.set(selected_dir)
    validate_fields()


def show_or_hide_degrees(event=None):
    selection = incline_var.get()
    if selection == "Level":
        degree_container.pack_forget()
    else:
        degree_container.pack(anchor="w")
    validate_fields()


def update_timer():
    global countdown_seconds
    if countdown_seconds >= 0:
        timer_label.config(text=f"Recording... {countdown_seconds} sec remaining")
        root.after(1000, update_timer)
        countdown_seconds -= 1


def recording_finished():
    progress_bar.stop()
    progress_bar.pack_forget()
    timer_label.pack_forget()
    start_button.pack(pady=(0, 20))
    status_label.config(text="Recording finished!", foreground="green")


def check_exoskeleton_connection():
    global exoskeleton_port_name
    try:
        result = fp.is_exoskeleton_connected()
        if result:
            exoskeleton_port_name = result
            connected_label.config(text="Exoskeleton Connected")
            retry_button.config(state="disabled")
        else:
            exoskeleton_port_name = None
            connected_label.config(text="Exoskeleton Not Connected")
            retry_button.config(state="normal")
    except Exception as e:
        exoskeleton_port_name = None
        connected_label.config(text="Exoskeleton Error")
        retry_button.config(state="normal")
        messagebox.showerror("Connection Error", str(e))
    validate_fields()


# ───────────── Start Test ─────────────
def on_start():
    validate_fields()
    if start_button["state"] == "disabled":
        messagebox.showerror("Invalid Input", status_label["text"])
        return

    check_exoskeleton_connection()
    if not exoskeleton_port_name:
        messagebox.showerror(
            "Exoskeleton Not Connected", "No exoskeleton port available."
        )
        return

    start_button.pack_forget()
    timer_label.pack()
    progress_bar.pack()
    progress_bar.start(10)

    name_parts = patient_var.get().split()
    first, middle, last = "", "", ""
    if len(name_parts) == 3:
        first, middle, last = name_parts
    elif len(name_parts) == 2:
        first, last = name_parts

    speed = speed_var.get()
    incline_status = incline_var.get()
    degrees = degree_var.get() if incline_status != "Level" else ""

    parts = [first]
    if middle:
        parts.append(middle)
    parts.extend([last, speed, incline_status])
    if degrees:
        parts.append(degrees)
    testname = "_".join(parts)

    total_time = int(duration_var.get())
    port = exoskeleton_port_name

    def record_task():
        try:
            print(directory_var.get)
            DR.record_to_csv(
                testname=directory_var + testname, total_time=total_time, port=port
            )
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Exoskeleton Error", f"{e}"))
        finally:
            root.after(0, recording_finished)

    global countdown_seconds
    countdown_seconds = total_time
    update_timer()
    threading.Thread(target=record_task, daemon=True).start()


# ───────────── GUI Setup ─────────────
root = tk.Tk()
root.title("Exoskeleton Treadmill Data Collection App")
root.geometry("1000x600")
root.columnconfigure((0, 1, 2), weight=1, uniform="column")
root.rowconfigure(0, weight=1)

blue_color = "#0055A2"
gold_color = "#C99700"
gray_color = "#A7A8AA"
font_style = ("Helvetica", 16)

style = ttk.Style()
style.theme_use("clam")
for theme in ["Blue", "Gold", "Gray"]:
    color = locals()[f"{theme.lower()}_color"]
    style.configure(f"{theme}.TLabelframe", background=color, font=font_style)
    style.configure(f"{theme}.TLabelframe.Label", background=color, font=font_style)
    style.configure(f"{theme}.TFrame", background=color)
    style.configure(f"{theme}.TLabel", background=color, font=font_style)
    style.configure(f"{theme}.TButton", font=font_style)
style.configure("TEntry", font=font_style)

# ───────────── Panels and Fields ─────────────
patient_list = load_patient_names()
default_patient = patient_list[-1] if patient_list else "No Patients Loaded"

# Left Panel
connect_wrapper = ttk.LabelFrame(root, text="Status Panel", style="Blue.TLabelframe")
connect_wrapper.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
connect_frame = ttk.Frame(connect_wrapper, style="Blue.TFrame")
connect_frame.pack(fill="both", expand=True, padx=10, pady=10)
connected_label = ttk.Label(connect_frame, text="Checking...", style="Blue.TLabel")
connected_label.pack(pady=10)
retry_button = ttk.Button(
    connect_frame,
    text="Retry",
    style="Blue.TButton",
    command=check_exoskeleton_connection,
)
retry_button.pack(pady=10)

# Middle Panel
middle_wrapper = ttk.LabelFrame(
    root, text="Treadmill Configuration", style="Gold.TLabelframe"
)
middle_wrapper.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
middle_frame = ttk.Frame(middle_wrapper, style="Gold.TFrame")
middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(middle_frame, text="Select Patient:", style="Gold.TLabel").pack(anchor="w")
patient_var = tk.StringVar(value=default_patient)
patient_dropdown = ttk.Combobox(middle_frame, textvariable=patient_var, font=font_style)
patient_dropdown["values"] = patient_list if patient_list else ["No Patients Loaded"]
patient_dropdown.pack(fill="x", pady=(0, 15))

ttk.Label(middle_frame, text="Set Treadmill Speed:", style="Gold.TLabel").pack(
    anchor="w"
)
speed_var = tk.StringVar(value="3")
speed_entry = ttk.Entry(middle_frame, textvariable=speed_var, width=10, font=font_style)
speed_entry.pack(anchor="w")
ttk.Label(middle_frame, text="mph", style="Gold.TLabel").pack(anchor="w")
speed_var.trace_add("write", lambda *args: enforce_decimal_limit(speed_var))

ttk.Label(middle_frame, text="Elevation:", style="Gold.TLabel").pack(anchor="w")
incline_var = tk.StringVar(value="Level")
incline_dropdown = ttk.Combobox(
    middle_frame, textvariable=incline_var, font=font_style, width=15
)
incline_dropdown["values"] = ("Incline", "Level", "Decline")
incline_dropdown.pack(anchor="w")
incline_dropdown.bind("<<ComboboxSelected>>", show_or_hide_degrees)

degree_container = ttk.Frame(middle_frame, style="Gold.TFrame")
degree_var = tk.StringVar(value="0")
ttk.Entry(degree_container, textvariable=degree_var, width=10, font=font_style).pack(
    side="left"
)
ttk.Label(degree_container, text="Degrees", style="Gold.TLabel").pack(
    side="left", padx=(5, 0)
)
degree_var.trace_add("write", lambda *args: enforce_decimal_limit(degree_var))

# Right Panel
right_wrapper = ttk.LabelFrame(root, text="Run Settings", style="Gray.TLabelframe")
right_wrapper.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
right_frame = ttk.Frame(right_wrapper, style="Gray.TFrame")
right_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(right_frame, text="Enter Duration (sec):", style="Gray.TLabel").pack(
    anchor="w"
)
duration_var = tk.StringVar(value="10")
ttk.Entry(right_frame, textvariable=duration_var, width=10, font=font_style).pack(
    anchor="w", pady=(0, 15)
)

ttk.Label(right_frame, text="Save Data To:", style="Gray.TLabel").pack(anchor="w")
directory_var = tk.StringVar()
ttk.Entry(right_frame, textvariable=directory_var, width=25, font=font_style).pack(
    anchor="w", pady=(0, 5)
)
ttk.Button(
    right_frame, text="Browse...", command=browse_directory, style="Gray.TButton"
).pack(pady=(0, 10))

status_icon_label = ttk.Label(
    right_frame, text="", foreground="red", style="Gray.TLabel"
)
status_icon_label.pack()
status_label = ttk.Label(
    right_frame,
    text="",
    wraplength=300,
    justify="left",
    foreground="red",
    style="Gray.TLabel",
)
status_label.pack(anchor="w", pady=(0, 10))

timer_label = ttk.Label(right_frame, text="", style="Gray.TLabel")
progress_bar = ttk.Progressbar(right_frame, mode="indeterminate", length=250)

start_button = ttk.Button(
    right_frame, text="Start", state="disabled", command=on_start, style="Gray.TButton"
)
start_button.pack(pady=(0, 20))

# Watch variables
for var in [
    patient_var,
    speed_var,
    incline_var,
    degree_var,
    duration_var,
    directory_var,
]:
    var.trace_add("write", validate_fields)

# Init
check_exoskeleton_connection()
show_or_hide_degrees()
validate_fields()
root.mainloop()
