# Part 2: Initial Analysis - Data Overview

import sqlite3
import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns

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

# Part 3: Statistical Analysis

metadata_query = """
SELECT
    samples.sample,
    samples.subject,
    samples.sample_type,
    subjects.condition,
    subjects.treatment,
    subjects.response
FROM samples
JOIN subjects
    ON samples.subject = subjects.subject
"""

metadata = pd.read_sql_query(metadata_query, conn)

# Combine the Part 2 summary with the sample metadata
analysis_data = summary.merge(metadata, on="sample")

# Only include PBMC samples.
filtered_data = analysis_data[
    (analysis_data["condition"] == "melanoma")
    & (analysis_data["treatment"] == "miraclib")
    & (analysis_data["sample_type"] == "PBMC")
]

# Compare responders and non-responders for each cell population
results = []

# go through each cell population and perform the Mann-Whitney U test
for population in cell_columns: 

    population_data = filtered_data[
        filtered_data["population"] == population
    ]

    responders = population_data[
        population_data["response"] == "yes"
    ]["percentage"]

    non_responders = population_data[
        population_data["response"] == "no"
    ]["percentage"]

    # run test and store the results
    statistic, p_value = mannwhitneyu(
        responders,
        non_responders,
        alternative="two-sided"
    )

    results.append({
        "population": population,
        "statistic": statistic,
        "p_value": p_value,
        "significant": p_value < 0.05 # Mark significant results
    })

results_df = pd.DataFrame(results)

# Create boxplots comparing responders vs non-responders
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=filtered_data,
    x="population", # cell population on x-axis
    y="percentage", # relative frequency on y-axis
    hue="response" # yes or no
)

plt.title("Cell Population Frequencies: Responders vs Non-Responders")
plt.xlabel("Cell Population")
plt.ylabel("Relative Frequency (%)")

plt.tight_layout()
plt.savefig("cell_population_boxplot.png")

plt.close()

print("\nSamples by response:")
print(filtered_data.groupby("response")["sample"].nunique())

print("\nStatistical results:")
print(results_df)

conn.close()
