import tkinter as tk
from tkinter import ttk, messagebox
from utils import load_patient_dataframe, save_patient_dataframe


class ViewPatientsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(style="Blue.TFrame")
        title = ttk.Label(
            self, text="All Patients", font=("Helvetica", 20), style="Blue.TLabel"
        )
        title.pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("Patient_Name", "Gender", "Date of Birth", "Phone", "Email"),
            show="headings",
        )

        self.tree.heading("Patient_Name", text="Patient Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Date of Birth", text="Date of Birth")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.tag_configure("even", background="#E8E8E8")
        self.tree.tag_configure("odd", background="#FFFFFF")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        btn_frame = ttk.Frame(self, style="Blue.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame, text="Delete Selected", command=self.delete_selected
        ).pack(side="left", padx=10)
        ttk.Button(
            btn_frame, text="Back", command=lambda: controller.show_frame("MainMenu")
        ).pack(side="left", padx=10)

    def on_show(self):
        self.populate_treeview()

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        info_df, data_df = load_patient_dataframe()

        print(info_df)
        if info_df.empty:
            return

        for (_, info_row), (_, data_row) in zip(info_df.iterrows(), data_df.iterrows()):

            middle = info_row.get("Middle Name", "")
            print(type(middle))
            if isinstance(middle, str) and middle.strip():
                middle_initial = f"{middle.strip()[0]}."
            else:
                middle_initial = ""
            # middle_initial = (
            #    f"{str(middle).strip()[0]}." if middle and middle.strip() else ""
            # )

            if middle_initial == "":
                name = (
                    f"{info_row.get('First Name', '')} {info_row.get('Last Name', '')}"
                )
            else:
                name = f"{info_row.get('First Name', '')} {middle_initial} {info_row.get('Last Name', '')}"

            # self.tree.insert(
            #    "",
            #    "end",
            #    values=(pid, name.strip(), row.get("Phone", ""), row.get("Email", "")),
            # )
            gender = data_row.get("gender", "")
            DOB = data_row.get("dob", "")

            # Since phone humber is a Float per the DF

            if info_row.get("Phone") and str(info_row.get("Phone")).strip():
                phone_number = str(info_row.get("Phone")).strip()[0:10]
                phone_string = (
                    f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
                )
            else:
                phone_string = "-"

            self.tree.insert(
                "",
                "end",
                values=(
                    name.strip(),
                    gender,
                    DOB,
                    phone_string,
                    (
                        info_row.get("Email")
                        if info_row.get("Email") and str(info_row.get("Email")).strip()
                        else "-" if isinstance(info_row.get("Email"), str) else "-"
                    ),
                ),
            )

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete the selected patient(s)?"
        )
        if not confirm:
            return

        ids_to_delete = [self.tree.item(item)["values"][0] for item in selected]

        info_df, data_df = load_patient_dataframe()
        info_df = info_df[~info_df["Patient_ID"].isin(ids_to_delete)]
        data_df = data_df[~data_df["Patient_ID"].isin(ids_to_delete)]

        save_patient_dataframe(info_df, data_df)
        self.populate_treeview()
