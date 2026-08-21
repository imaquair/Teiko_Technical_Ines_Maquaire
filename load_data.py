# Data Management
# This script initializes the database with a specific schema and loads all rows from cell-count.csv.
# Each row is one biological sample from a single patient. 

import sqlite3
import pandas as pd

# Step 1: Create a database
conn = sqlite3.connect("cell_counts.db")

# Step 2: Create the tables
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    subject_id TEXT PRIMARY KEY,
    project_id TEXT,
    condition TEXT,
    age INTEGER,
    sex TEXT,
    treatment TEXT,
    response TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS samples (
    sample_id TEXT PRIMARY KEY,
    subject_id TEXT,
    sample_type TEXT,
    time_from_treatment_start INTEGER,
    b_cell INTEGER,
    cd8_t_cell INTEGER,
    cd4_t_cell INTEGER,
    nk_cell INTEGER,
    monocyte INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
""")

# Step 3: read the CSV and insert the data into the database

df = pd.read_csv("cell-count.csv")
print(df.head())

projects = df["project"].drop_duplicates()
for project in projects:
    cursor.execute(
        "INSERT OR IGNORE INTO projects (project_id) VALUES (?)",
        (project,)
    )

subjects = df[
    ["subject", "project", "condition", "age", "sex", "treatment", "response"]
].drop_duplicates(subset=["subject"])

for _, row in subjects.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO subjects
        (subject_id, project_id, condition, age, sex, treatment, response)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["subject"],
        row["project"],
        row["condition"],
        row["age"],
        row["sex"],
        row["treatment"],
        row["response"]
    ))

for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO samples
        (sample_id, subject_id, sample_type, time_from_treatment_start,
         b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["sample"],
        row["subject"],
        row["sample_type"],
        row["time_from_treatment_start"],
        row["b_cell"],
        row["cd8_t_cell"],
        row["cd4_t_cell"],
        row["nk_cell"],
        row["monocyte"]
    ))

conn.commit()

print("Database created successfully.")
print(f"Loaded {len(df)} samples.")

cursor.execute("SELECT COUNT(*) FROM samples")
sample_count = cursor.fetchone()[0]
print(f"Samples in database: {sample_count}")


conn.close()