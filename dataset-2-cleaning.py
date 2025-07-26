import sqlite3
import csv

# Connect to an in-memory SQLite database
con = sqlite3.connect(':memory:')
cursor = con.cursor()

# Create the SQL table
fields_to_insert = ["Name", "Orbit Height (km)", "Repeat Cycle (days)", "Launched in", "Out of service since", "Organisation"]
with open('Dataset-2.csv', newline='') as ds2:
    reader = csv.reader(ds2)
    headers = next(reader)
    indices = [headers.index(field) for field in fields_to_insert]

    cursor.execute("""
        CREATE TABLE Satellite (
            [Name] TEXT PRIMARY KEY,
            [Orbit Height (km)] INTEGER,
            [Repeat Cycle (days)] INTEGER,
            [Launched in] INTEGER,
            [Out of service since (years)] INTEGER,
            [Organisation] TEXT,
            [Company] TEXT,
            [Country] TEXT
        )
    """)
    for row in reader:
        selected_row = [row[i] for i in indices]
        # Handle missing values in Repeat Cycle
        """Placeholder"""
        # Split organisation into company and country
        full_organisation = row[-1]
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
            cursor.execute("INSERT INTO Satellite VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (*selected_row, company, country))

# Thanks ChatGPT

with open('exported_satellites.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    cursor.execute("PRAGMA table_info(Satellite)")
    headers = [info[1] for info in cursor.fetchall()]
    writer.writerow(headers)
    # Write data rows
    cursor.execute("SELECT * FROM Satellite")
    writer.writerows(cursor.fetchall())