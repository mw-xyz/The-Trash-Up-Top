import sqlite3
import csv

# Connect to an in-memory SQLite database
con = sqlite3.connect(':memory:')
cursor = con.cursor()

# Example for loading 'AllSatellites.csv'
with open('Dataset-2.csv', newline='') as ds2:
    reader = csv.reader(ds2)
    cursor.execute("CREATE TABLE Satellite(" \
    "Name VARCHAR(50) PRIMARY KEY," \
    "OrbitHeight (km) integer," \
    "RepeatCycle (days) integer," \
    "YearOflaunch ")