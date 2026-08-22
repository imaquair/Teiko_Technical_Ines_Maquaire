import streamlit as st
import pandas as pd

st.title("Immune Cell Analysis Dashboard")

st.write(
    "Interactive results for cell population frequencies, "
    "treatment response analysis, and baseline sample summaries."
)

# Load Part 2 results
summary = pd.read_csv("outputs/cell_frequencies.csv")

st.header("Part 2: Cell Population Frequencies")

# Let the user choose a sample
sample_options = summary["sample"].unique()
selected_sample = st.selectbox("Select a sample:", sample_options)

# Show only the selected sample
sample_data = summary[summary["sample"] == selected_sample]

st.dataframe(sample_data)

# Display relative cell frequencies for the selected sample
st.subheader("Relative Cell Frequencies")

st.bar_chart(
    sample_data,
    x="population",
    y="percentage"
)

# Load Part 3 results

st.header("Part 3: Responders vs Non-Responders")

results = pd.read_csv("outputs/statistical_results.csv")

st.subheader("Statistical Results")
st.dataframe(results)

st.write(
    "At a significance threshold of p < 0.05, "
    "CD4 T cells showed a statistically significant difference "
    "between responders and non-responders."
)

st.subheader("Relative Frequencies by Response")

st.image(
    "outputs/cell_population_boxplot.png",
    caption="Relative cell population frequencies for responders vs non-responders"
)

# Load Part 4 results
st.header("Part 4: Baseline Subset Analysis")

baseline_data = pd.read_csv("outputs/baseline_samples.csv")

st.write(f"Total baseline samples: {len(baseline_data)}")

# Samples by project
samples_by_project = baseline_data["project"].value_counts()

st.subheader("Samples by Project")
st.dataframe(samples_by_project.reset_index())

# Subjects by response
subjects_by_response = (
    baseline_data
    .groupby("response")["subject"]
    .nunique()
)

st.subheader("Subjects by Response")
st.dataframe(subjects_by_response.reset_index())

# Subjects by sex
subjects_by_sex = (
    baseline_data
    .groupby("sex")["subject"]
    .nunique()
)

st.subheader("Subjects by Sex")
st.dataframe(subjects_by_sex.reset_index())