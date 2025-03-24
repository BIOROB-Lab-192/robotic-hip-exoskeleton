import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import pandas as pd
import os
import find_ports as fp


def load_patient_names():
    filename = "data/patient_info.xlsx"
    if not os.path.exists(filename):
        return []

    try:
        df = pd.read_excel(filename)
        df.columns = df.columns.str.strip()  # Clean up headers

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
        print("Error loading patient_info.xlsx:", e)
        return []


def show_or_hide_degrees(event=None):
    selection = incline_var.get()
    if selection == "Level":
        degree_container.pack_forget()
    else:
        degree_container.pack(anchor="w")
    validate_fields()


def browse_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        directory_var.set(selected_dir)
    validate_fields()


def is_valid_decimal(value, max_decimals=1):
    if re.fullmatch(r"\d+\.\d{%d,}" % (max_decimals + 1), value):
        return False
    if re.fullmatch(r"\d+\.\d{0,%d}" % max_decimals, value):
        return True
    if re.fullmatch(r"\d+", value):
        return True
    if re.fullmatch(r"\d+\.", value):
        return True
    return False


def enforce_decimal_limit(var, max_decimals=1):
    value = var.get()
    if not re.fullmatch(r"\d*(\.\d{0,%d})?" % max_decimals, value):
        var.set(value[:-1])


def validate_fields(*args):
    errors = []

    if not patient_list:
        errors.append("• No patients loaded from file")

    try:
        speed = speed_var.get()
        if not is_valid_decimal(speed):
            raise ValueError("Speed must be a number with at most 1 decimal place")
        speed = float(speed)
        if not (0 <= speed <= 10):
            raise ValueError("Speed must be between 0 and 10 mph")
    except ValueError as e:
        errors.append(f"• {str(e)}")

    if incline_var.get() != "Level":
        try:
            degrees = degree_var.get()
            if not is_valid_decimal(degrees):
                raise ValueError(
                    "Degrees must be a number with at most 1 decimal place"
                )
            degrees = float(degrees)
            if not (0 <= degrees < 30):
                raise ValueError("Elevation must be less than 30 degrees")
        except ValueError as e:
            errors.append(f"• {str(e)}")

    if not duration_var.get():
        errors.append("• Duration is required")

    if not directory_var.get():
        errors.append("• Save directory is required")

    if errors:
        status_icon_label.configure(text="⚠", foreground="red")
        status_label.configure(text="\n".join(errors), foreground="red")
        start_button.config(state="disabled")
    else:
        status_icon_label.configure(text="", foreground="green")
        status_label.configure(text="Ready to start", foreground="green")
        start_button.config(state="normal")


def on_start():
    validate_fields()
    if start_button["state"] == "disabled":
        messagebox.showerror("Invalid Input", status_label["text"])
        return
    messagebox.showinfo("Starting", "Test started successfully!")


# ────────────────────── GUI Setup ──────────────────────

root = tk.Tk()
root.title("Exoskeleton Treadmill Data Collection App")
root.geometry("1000x600")
root.columnconfigure((0, 1, 2), weight=1, uniform="column")
root.rowconfigure(0, weight=1)

# Colors and Fonts
blue_color = "#0055A2"
gold_color = "#C99700"
gray_color = "#A7A8AA"
font_style = ("Helvetica", 16)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Blue.TLabelframe", background=blue_color, foreground="white", font=font_style
)
style.configure(
    "Blue.TLabelframe.Label", background=blue_color, foreground="white", font=font_style
)
style.configure("Blue.TFrame", background=blue_color)
style.configure(
    "Blue.TLabel", background=blue_color, foreground="white", font=font_style
)
style.configure("Blue.TButton", font=font_style)

style.configure(
    "Gold.TLabelframe", background=gold_color, foreground="black", font=font_style
)
style.configure(
    "Gold.TLabelframe.Label", background=gold_color, foreground="black", font=font_style
)
style.configure("Gold.TFrame", background=gold_color)
style.configure(
    "Gold.TLabel", background=gold_color, foreground="black", font=font_style
)
style.configure("Gold.TButton", font=font_style)

style.configure(
    "Gray.TLabelframe", background=gray_color, foreground="black", font=font_style
)
style.configure(
    "Gray.TLabelframe.Label", background=gray_color, foreground="black", font=font_style
)
style.configure("Gray.TFrame", background=gray_color)
style.configure(
    "Gray.TLabel", background=gray_color, foreground="black", font=font_style
)
style.configure("Gray.TButton", font=font_style)

style.configure("TEntry", font=font_style)

# Load Patients
patient_list = load_patient_names()
default_patient = patient_list[-1] if patient_list else "No Patients Loaded"

# Left Panel
connect_wrapper = ttk.LabelFrame(root, text="Status Panel", style="Blue.TLabelframe")
connect_wrapper.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
connect_frame = ttk.Frame(connect_wrapper, style="Blue.TFrame")
connect_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(
    connect_frame, text="Exoskeleton Connected", style="Blue.TLabel", justify="left"
).pack(anchor="w", pady=10)
ttk.Button(connect_frame, text="Retry", style="Blue.TButton").pack(pady=10)

# Middle Panel
middle_wrapper = ttk.LabelFrame(
    root, text="Treadmill Configuration", style="Gold.TLabelframe"
)
middle_wrapper.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
middle_frame = ttk.Frame(middle_wrapper, style="Gold.TFrame")
middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(
    middle_frame, text="Select Patient:", style="Gold.TLabel", justify="left"
).pack(anchor="w", pady=(0, 5))
patient_var = tk.StringVar(value=default_patient)
patient_dropdown = ttk.Combobox(
    middle_frame, textvariable=patient_var, font=font_style, justify="left"
)
patient_dropdown["values"] = patient_list if patient_list else ["No Patients Loaded"]
patient_dropdown.pack(fill="x", pady=(0, 15))

ttk.Label(middle_frame, text="Set Treadmill Speed:", style="Gold.TLabel").pack(
    anchor="w", pady=(0, 5)
)
speed_frame = ttk.Frame(middle_frame, style="Gold.TFrame")
speed_frame.pack(fill="x", pady=(0, 15))
speed_var = tk.StringVar(value="3")
speed_entry = ttk.Entry(
    speed_frame, textvariable=speed_var, width=10, font=font_style, justify="left"
)
speed_entry.pack(side="left")
ttk.Label(speed_frame, text="mph", style="Gold.TLabel").pack(side="left", padx=(5, 0))
speed_var.trace_add("write", lambda *args: enforce_decimal_limit(speed_var))

ttk.Label(middle_frame, text="Elevation:", style="Gold.TLabel").pack(
    anchor="w", pady=(0, 5)
)
incline_frame = ttk.Frame(middle_frame, style="Gold.TFrame")
incline_frame.pack(fill="x", pady=(0, 15))

incline_var = tk.StringVar(value="Level")
incline_dropdown = ttk.Combobox(
    incline_frame, textvariable=incline_var, width=15, font=font_style, justify="left"
)
incline_dropdown["values"] = ("Incline", "Level", "Decline")
incline_dropdown.pack(side="left", padx=(0, 10))
incline_dropdown.bind("<<ComboboxSelected>>", show_or_hide_degrees)

degree_container = ttk.Frame(incline_frame, style="Gold.TFrame")
degree_var = tk.StringVar(value="0")
degree_entry = ttk.Entry(
    degree_container, textvariable=degree_var, width=10, font=font_style, justify="left"
)
degree_entry.pack(side="left")
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
    anchor="w", pady=(5, 5)
)
duration_var = tk.StringVar(value="10")
ttk.Entry(
    right_frame, textvariable=duration_var, width=10, font=font_style, justify="left"
).pack(anchor="w", pady=(0, 15))

ttk.Label(right_frame, text="Save Data To:", style="Gray.TLabel").pack(
    anchor="w", pady=(10, 5)
)
directory_var = tk.StringVar()
ttk.Entry(
    right_frame, textvariable=directory_var, width=25, font=font_style, justify="left"
).pack(anchor="w", pady=(0, 5))
ttk.Button(
    right_frame, text="Browse...", command=browse_directory, style="Gray.TButton"
).pack(pady=(0, 20))

status_icon_label = ttk.Label(
    right_frame, text="", foreground="red", style="Gray.TLabel", justify="left"
)
status_icon_label.pack(pady=[5, 0])
status_label = ttk.Label(
    right_frame,
    text="",
    wraplength=300,
    justify="left",
    foreground="red",
    style="Gray.TLabel",
)
status_label.pack(anchor="w", pady=(0, 10))

start_button = ttk.Button(
    right_frame, text="Start", state="disabled", command=on_start, style="Gray.TButton"
)
start_button.pack(pady=(0, 20))

for var in [
    patient_var,
    speed_var,
    incline_var,
    degree_var,
    duration_var,
    directory_var,
]:
    var.trace_add("write", validate_fields)

show_or_hide_degrees()
validate_fields()
root.mainloop()
