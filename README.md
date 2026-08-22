# Teiko Technical — Ines Maquaire

## Interactive Dashboard

The interactive Streamlit dashboard displays the results from Parts 2–4, including cell population frequencies, responder vs. non-responder comparisons, statistical results, and baseline subset analysis.
[View the Interactive Dashboard](https://teikotechnicalinesmaquaire.streamlit.app/) (https://teikotechnicalinesmaquaire.streamlit.app/)

## Running the Project

The project can be run from the repository root using the provided Makefile.

### 1. Install Dependencies

Install all required Python dependencies:

```bash
make setup
```

### 2. Run the Data Pipeline

Run the complete pipeline, including database creation, data loading, analysis, statistical testing, and output generation:

```bash
make pipeline
```

This generates the SQLite database and the required output tables and plots for Parts 1–4.

### 3. Start the Dashboard

Start the interactive Streamlit dashboard:

```bash
make dashboard
```

The dashboard will start a local Streamlit server and can be opened using the URL displayed in the terminal.

## Project Structure

- `load_data.py` — Creates the SQLite database, initializes the schema, and loads `cell-count.csv`.
- `analysis.py` — Performs the analyses for Parts 2–4, including cell frequency calculations, statistical testing, visualization, and subset analysis.
- `dashboard.py` — Runs the interactive Streamlit dashboard.
- `requirements.txt` — Lists the Python dependencies required to run the project.
- `Makefile` — Provides commands to install dependencies, run the full pipeline, and start the dashboard.
- `outputs/` — Contains generated analysis tables and plots.

The project separates data loading, analysis, and visualization so that each part has a clear responsibility. The full workflow can be reproduced automatically using the Makefile.

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


## Part 3: Statistical Analysis

The analysis compares **immune cell population relative frequencies between responders and non-responders**.

The data is filtered to include only:

- **Condition:** Melanoma
- **Treatment:** Miraclib
- **Sample type:** PBMC

Responder status is determined using the `response` column, where `yes` represents responders and `no` represents non-responders.

### Statistical Testing

For each immune cell population, a **two-sided Mann–Whitney U test** is used to compare relative frequencies between responders and non-responders. A significance threshold of `p < 0.05` is used.

The results are:

| Population | U Statistic | p-value | Significant |
|---|---:|---:|---|
| b_cell | 459975.5 | 0.0557 | No |
| cd8_t_cell | 478178.0 | 0.6392 | No |
| cd4_t_cell | 515255.0 | 0.0134 | Yes |
| nk_cell | 464546.5 | 0.1211 | No |
| monocyte | 466525.0 | 0.1635 | No |

At the unadjusted p < 0.05 significance level, CD4 T cells are the only population with a statistically significant difference in relative frequency between responders and non-responders (p = 0.0134). Because five cell populations were tested, this result should be interpreted cautiously as evidence of an association rather than proof that CD4 T-cell frequency predicts treatment response.

### Visualization

A boxplot is generated to compare the relative frequency distributions of each immune cell population between responders and non-responders. The plot is saved as `outputs/cell_population_boxplot.png`.

### Running the Statistical Analysis

From the repository root, run: python analysis.py

## Part 4: Data Subset Analysis

The analysis identifies **baseline melanoma PBMC samples from patients treated with miraclib** using the following filters:

- **Condition:** Melanoma
- **Treatment:** Miraclib
- **Sample type:** PBMC
- **Time from treatment start:** 0

A total of **656 baseline samples** met these criteria.

### Baseline Sample Summary

- **Samples by project:**
  - prj1: 384
  - prj3: 272

- **Subjects by response:**
  - Responders: 331
  - Non-responders: 325

- **Subjects by sex:**
  - Female: 312
  - Male: 344

### Additional B-Cell Analysis

For the additional question, the analysis considers **male melanoma responders at time 0 across all sample and treatment types**.

The average B-cell count for these samples is: **10,206.15**

### Running the Analysis

From the repository root, run:python analysis.py