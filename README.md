# Teiko_Technical_Ines_Maquaire

## Part 1: Data Management

The data is stored in a **SQLite relational database** using three related tables:

- **Projects** — Stores each unique project.
- **Subjects** — Stores patient-level information, including condition, age, sex, treatment, and response. Each subject belongs to a project.
- **Samples** — Stores individual biological samples, including sample type, time from treatment start, and the five immune cell counts. Each sample belongs to a subject.

The database follows the relationship: `Project → Subject → Sample`

### Schema Design and Rationale

The schema separates project, subject, and sample information based on the level at which each attribute belongs. A project can contain multiple subjects, and a subject can have multiple biological samples collected at different time points.

The **Subjects** table contains attributes that remain constant for a subject in the provided dataset, such as age, sex, condition, treatment, and response. The **Samples** table contains sample-specific information, including collection time, sample type, and immune cell counts.

Separating these entities avoids repeating the same project and patient information for every sample. Primary and foreign keys maintain the relationships between the tables and make it straightforward to combine them when performing analyses.

This design can scale to larger datasets containing hundreds of projects and thousands of samples. New projects, subjects, and samples can be added without changing the overall database structure. Additional tables or indexes could also be added as the dataset and analytical requirements grow.

### Running the Data Loader: 
From the repository root, run: python load_data.py



## Part 2: Initial Analysis - Data Overview

The analysis calculates the **relative frequency of each immune cell population for every sample**.

For each sample:

1. The five immune cell counts are summed to calculate the `total_count`.
2. The data is reshaped so each cell population has its own row.
3. The relative frequency is calculated as:

`percentage = (count / total_count) × 100` 

The resulting summary table contains:

- **sample** — Sample identifier
- **total_count** — Total number of cells in the sample
- **population** — Immune cell population
- **count** — Number of cells in that population
- **percentage** — Relative frequency of the population (rounded to 2 decimal places for better readability)

### Running the Initial Analysis: 
From the repository root, run: python analysis.py