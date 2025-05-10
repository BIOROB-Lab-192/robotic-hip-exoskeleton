import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from utils import load_patient_dataframe, update_patient_dataframe


class ViewPatientsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="Blue.TFrame")

        ttk.Label(
            self, text="All Patients", font=("Helvetica", 20), style="Blue.TLabel"
        ).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=(
                "Patient_ID",
                "Patient_Name",
                "Gender",
                "Date of Birth",
                "Phone",
                "Email",
            ),
            show="headings",
        )
        self.tree.heading("Patient_ID", text="Patient ID")
        self.tree.column("Patient_ID", width=0, stretch=False)
        self.tree.heading("Patient_Name", text="Patient Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Date of Birth", text="Date of Birth")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        btn_frame = ttk.Frame(self, style="Blue.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame, text="Delete Selected", command=self.delete_selected
        ).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected).pack(
            side="left", padx=10
        )
        ttk.Button(
            btn_frame, text="Back", command=lambda: controller.show_frame("MainMenu")
        ).pack(side="left", padx=10)

    def on_show(self):
        self.populate_treeview()

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        info_df, data_df = load_patient_dataframe()

        if info_df.empty:
            print("Info DataFrame is empty")
            return

        for (_, info_row), (_, data_row) in zip(info_df.iterrows(), data_df.iterrows()):
            pid = str(info_row.get("Patient_ID", ""))
            middle = info_row.get("Middle Name", "")
            middle_initial = (
                f"{str(middle).strip()[0]}."
                if pd.notna(middle) and str(middle).strip()
                else ""
            )
            name = f"{info_row.get('First Name', '')} {middle_initial} {info_row.get('Last Name', '')}".strip()

            gender = data_row.get("gender", "")
            dob = data_row.get("dob", "")

            phone = info_row.get("Phone", "")
            phone_string = "-"
            if pd.notna(phone) and phone.strip().isdigit():
                phone_number = phone.zfill(10)[:10]
                phone_string = (
                    f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
                )

            email = info_row.get("Email", "")
            email_display = email if pd.notna(email) and str(email).strip() else "-"

            self.tree.insert(
                "",
                "end",
                iid=pid,
                values=(pid, name, gender, dob, phone_string, email_display),
            )

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a patient to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete the selected patient(s)?"
        )
        if not confirm:
            return

        ids_to_delete = [
            str(self.tree.item(iid)["values"][0]) for iid in selected_items
        ]

        info_df, data_df = load_patient_dataframe()
        initial_count = len(info_df)
        info_df["Patient_ID"] = info_df["Patient_ID"].astype(str)
        data_df["Patient_ID"] = data_df["Patient_ID"].astype(str)

        info_df = info_df[~info_df["Patient_ID"].isin(ids_to_delete)]
        data_df = data_df[~data_df["Patient_ID"].isin(ids_to_delete)]

        if len(info_df) < initial_count:
            update_patient_dataframe(info_df, data_df)
            self.populate_treeview()
            messagebox.showinfo("Deleted", "Selected patient(s) deleted successfully.")
        else:
            messagebox.showerror(
                "Deletion Error", "No patient(s) were removed. IDs may not match."
            )

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to edit.")
            return

        selected_item = self.tree.item(selected[0])
        patient_id = selected_item["values"][0]

        from patient_edit import EditPatientPage

        # Create new edit page instance dynamically
        edit_page = EditPatientPage(self.controller.container, self.controller)
        edit_page.set_patient_by_id(str(patient_id))

        self.controller.frames["EditPatientPage"] = edit_page
        edit_page.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame("EditPatientPage")
