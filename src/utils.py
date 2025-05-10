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
    df = pd.read_csv(INFO_FILE, dtype={"Patient_ID": str, "Phone": str})
    return int(df["Patient_ID"].astype(int).max() + 1) if not df.empty else 1


def load_patient_names():
    ensure_data_files()
    df = pd.read_csv(INFO_FILE, dtype={"Patient_ID": str, "Phone": str})
    names = []
    for _, row in df.iterrows():
        first = str(row.get("First Name", "")).strip().title()
        middle = row.get("Middle Name", "")
        middle_initial = (
            f"{str(middle).strip()[0]}."
            if pd.notna(middle) and str(middle).strip()
            else ""
        )
        last = str(row.get("Last Name", "")).strip().title()

        if not first or not last:
            continue

        name = (
            f"{first} {middle_initial} {last}".strip()
            if middle_initial
            else f"{first} {last}".strip()
        )
        names.append(name)
    return names


def load_patient_dataframe():
    ensure_data_files()
    info_df = pd.read_csv(
        INFO_FILE, dtype={"Patient_ID": str, "Phone": str}, parse_dates=False
    )
    data_df = pd.read_csv(DATA_FILE, dtype={"Patient_ID": str}, parse_dates=False)

    if "Patient_ID" in info_df.columns:
        info_df = info_df[
            ["Patient_ID"] + [col for col in info_df.columns if col != "Patient_ID"]
        ]
    if "Patient_ID" in data_df.columns:
        data_df = data_df[
            ["Patient_ID"] + [col for col in data_df.columns if col != "Patient_ID"]
        ]

    return info_df, data_df


def update_patient_dataframe(info_df, data_df):
    info_df["Patient_ID"] = info_df["Patient_ID"].astype(str)
    data_df["Patient_ID"] = data_df["Patient_ID"].astype(str)

    if "Patient_ID" in info_df.columns:
        info_df = info_df[
            ["Patient_ID"] + [col for col in info_df.columns if col != "Patient_ID"]
        ]
    if "Patient_ID" in data_df.columns:
        data_df = data_df[
            ["Patient_ID"] + [col for col in data_df.columns if col != "Patient_ID"]
        ]

    data_df["dob"] = data_df["dob"].astype(str)
    data_df["date_enrolled"] = data_df["date_enrolled"].astype(str)

    info_df.to_csv(INFO_FILE, index=False)
    data_df.to_csv(DATA_FILE, index=False)
