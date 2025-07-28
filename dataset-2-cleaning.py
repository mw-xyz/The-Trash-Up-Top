import sqlite3
import csv

# Connect to an in-memory SQLite database
con = sqlite3.connect(':memory:')
cursor = con.cursor()

# Create the SQL table
fields_to_insert = [
    "Name", "Orbit Height (km)", "Repeat Cycle (days)",
    "Launched in", "Out of service since", "Organisation"
]
with open('Dataset-2.csv', newline='') as ds2:
    reader = csv.reader(ds2)
    headers = next(reader)
    indices = [headers.index(field) for field in fields_to_insert]
    orbit_height_idx = fields_to_insert.index("Orbit Height (km)")
    repeat_cycle_idx = fields_to_insert.index("Repeat Cycle (days)")
    out_of_service_idx = fields_to_insert.index("Out of service since")
    organisation_idx = fields_to_insert.index("Organisation")

    cursor.execute("""
        CREATE TABLE Satellite (
            [Name] TEXT PRIMARY KEY,
            [Orbit Height (km)] INTEGER,
            [Repeat Cycle (days)] INTEGER,
            [Launched in] INTEGER,
            [Out of service since (years)] INTEGER,
            [Organisation] TEXT,
            [Company] TEXT,
            [Country] TEXT,
            [Type of Orbit] TEXT
        )
    """)
    for row in reader:
        selected_row = [row[i] for i in indices]
        # Handle missing values in Repeat Cycle
        repeat_cycle = selected_row[repeat_cycle_idx]
        try:
            repeat_cycle = int(repeat_cycle)
        except (ValueError, TypeError):
            repeat_cycle = None
        selected_row[repeat_cycle_idx] = repeat_cycle
        # Handle out of service since...
        out_of_service = selected_row[out_of_service_idx]
        try:
            out_of_service = int(out_of_service)
        except (ValueError, TypeError):
            out_of_service = None
        selected_row[out_of_service_idx] = out_of_service
        # Create orbit types
        orbit_height = selected_row[orbit_height_idx]
        try:
            orbit_height = int(orbit_height)
            if 160 < orbit_height < 2000:
                orbit_type = "LEO"
            elif orbit_height == 35786 or selected_row[1] == "Geostationary":
                orbit_type = "GEO"
            elif 2000 <= orbit_height < 36000:
                orbit_type = "MEO"
            elif orbit_height <= 36000:
                orbit_type = "HEO"
            else:
                orbit_type = "Other"
        except (ValueError, TypeError):
            orbit_type = None

        # Split organisation into company and country
        full_organisation = selected_row[organisation_idx]
        parts = full_organisation.split(" - ")
        company = parts[0]
        if len(parts) > 1:
            country = parts[1]
        else:
            if company == "US Naval Research Lab":
                country = "USA"
            elif company == "ESA":
                country = "N/A"
            elif "Turkey" in company:
                company = "TUBITAK UZAY/STRI"
                country = "Turkey"
            elif "US" in company or "NOAA" in company:
                country = "USA"
            elif "UK" in company:
                country = "UK"
            elif any(org in company for org in ("EUMETSAT", "ImageSat International", "ESA")):
                country = "IGO"
            else:
                country = "N/A"

        # Send all new information into the database
        cursor.execute("INSERT INTO Satellite VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (*selected_row, company, country, orbit_type))

# Thanks ChatGPT

with open('dataset_2_cleaned.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    cursor.execute("PRAGMA table_info(Satellite)")
    headers = [info[1] for info in cursor.fetchall()]
    writer.writerow(headers)
    # Write data rows
    cursor.execute("SELECT * FROM Satellite")
    writer.writerows(cursor.fetchall())