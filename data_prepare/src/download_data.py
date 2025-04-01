import os
import shutil
import sqlite3
import pandas as pd
import requests
import yaml
from pyprojroot import here
from utils.load_config import LoadConfig

CFG = LoadConfig()

def update_dates(file, backup_file):
    shutil.copy(backup_file, file)
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table';", conn
    ).name.tolist()
    tdf = {}
    for t in tables:
        tdf[t] = pd.read_sql(f"SELECT * from {t}", conn)

    example_time = pd.to_datetime(
        tdf["flights"]["actual_departure"].replace("\\N", pd.NaT)
    ).max()
    current_time = pd.to_datetime("now").tz_localize(example_time.tz)
    time_diff = current_time - example_time

    tdf["bookings"]["book_date"] = (
        pd.to_datetime(tdf["bookings"]["book_date"].replace(
            "\\N", pd.NaT), utc=True)
        + time_diff
    )

    datetime_columns = [
        "scheduled_departure",
        "scheduled_arrival",
        "actual_departure",
        "actual_arrival",
    ]
    for column in datetime_columns:
        tdf["flights"][column] = (
            pd.to_datetime(tdf["flights"][column].replace(
                "\\N", pd.NaT)) + time_diff
        )

    for table_name, df in tdf.items():
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    del df
    del tdf
    conn.commit()
    conn.close()

    return file


def prepare_travel_sql_db(travel_db_url):
    """Loads the travel SQL database and saves it in the data folder in the project's main directory."""

    os.makedirs(here("/shared/data"), exist_ok=True)

    local_file = here(CFG.local_file)
    backup_file = here(CFG.backup_file)

    overwrite = False
    if overwrite or not os.path.exists(local_file):
        response = requests.get(travel_db_url)
        response.raise_for_status()  # Ensure the request was successful
        with open(local_file, "wb") as f:
            f.write(response.content)
        shutil.copy(local_file, backup_file)

    update_dates(local_file, backup_file)
    return None


def prepare_airline_faq(airline_policy_url):
    """fetches the swiss_faq.md file and save it locally."""

    # Fetching the file content
    response = requests.get(airline_policy_url)
    response.raise_for_status()

    # Saving the content locally as 'swiss_faq.md'
    file_path = here(CFG.doc_dir)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    return None