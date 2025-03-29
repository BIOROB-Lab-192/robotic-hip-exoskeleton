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
    try:
        df = pd.read_csv(INFO_FILE)
        return int(df["Patient_ID"].max()) + 1 if not df.empty else 1
    except:
        return 1


def load_patient_names():
    ensure_data_files()
    try:
        df = pd.read_csv(INFO_FILE)
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


def load_patient_dataframe():
    if os.path.exists(INFO_FILE):
        return pd.read_csv(INFO_FILE)
    else:
        return pd.DataFrame(
            columns=[
                "Patient_ID",
                "First Name",
                "Middle Name",
                "Last Name",
                "Phone",
                "email",
            ]
        )


def save_patient_dataframe(df):
    df.to_csv(INFO_FILE, index=False)
