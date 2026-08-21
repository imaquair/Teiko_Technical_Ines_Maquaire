# Part 2: Initial Analysis - Data Overview

import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("cell_counts.db")

# Query the sample data
query = """
SELECT
    sample,
    b_cell,
    cd8_t_cell,
    cd4_t_cell,
    nk_cell,
    monocyte
FROM samples
"""

df = pd.read_sql_query(query, conn)

# Calculate the total number of cells in each sample
df["total_count"] = (
    df["b_cell"]
    + df["cd8_t_cell"]
    + df["cd4_t_cell"]
    + df["nk_cell"]
    + df["monocyte"]
)

# Reshape the table so each cell population has its own row
cell_columns = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte"
]

summary = df.melt(
    id_vars=["sample", "total_count"],
    value_vars=cell_columns,
    var_name="population",
    value_name="count"
)

# now we can calculate the percentage of each cell population relative to the total count
# rounded to 2 decimal places for better readability
summary["percentage"] = (
    summary["count"] / summary["total_count"] * 100
).round(2)


print(summary.head())
print(f"Summary table has {len(summary)} rows.")

conn.close()
