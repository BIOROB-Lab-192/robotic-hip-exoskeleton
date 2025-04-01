import os
import pandas as pd

DATA_DIR = "data"
INFO_FILE = os.path.join(DATA_DIR, "patient_info.csv")
DATA_FILE = os.path.join(DATA_DIR, "patient_data.csv")


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(INFO_FILE) or os.path.getsize(INFO_FILE) == 0:
        pd.DataFrame(
            columns=[
                "Patient_ID",
                "First Name",
                "Middle Name",
                "Last Name",
                "Phone",
                "Email",
            ]
        ).to_csv(INFO_FILE, index=False)
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
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
        ).to_csv(DATA_FILE, index=False)


def get_next_patient_id():
    ensure_data_files()
    df = pd.read_csv(INFO_FILE, dtype={"Phone": str, "Patient_ID": str})
    return int(df["Patient_ID"].max() + 1) if not df.empty else 1


def load_patient_names():
    ensure_data_files()
    df = pd.read_csv(INFO_FILE, dtype={"Phone": str, "Patient_ID": str})
    names = []
    for _, row in df.iterrows():

        first = str(row.get("First Name", "")).strip().title()
        middle = row.get("Middle Name", "")
        if isinstance(middle, str) and middle.strip():
            middle_initial = f"{middle.strip()[0]}."
        else:
            middle_initial = ""
        last = str(row.get("Last Name", "")).strip().title()
        if not first or not last:
            continue

        if middle_initial == "":
            name = f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip()
        else:
            name = f"{row.get('First Name', '')} {middle_initial} {row.get('Last Name', '')}".strip()

        names.append(name)
    return names


def load_patient_dataframe():
    ensure_data_files()
    info_df = pd.read_csv(INFO_FILE, dtype={"Phone": str, "Patient_ID": str})
    data_df = pd.read_csv(DATA_FILE, dtype={"Patient_ID": str})
    return info_df, data_df


def save_patient_dataframe(info_df, data_df):
    info_df.to_csv(INFO_FILE, index=False)
    data_df.to_csv(DATA_FILE, index=False)
