import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("FieldValuesExport_MultipleFiles.csv")

# View initial rows and structure
print(df.head())
print(df.info())

# Analyze unique values and counts for each column
column_analysis = {}
for column in df.columns:
    unique_values = df[column].nunique()  # Number of unique values
    counts = df[column].value_counts()    # Frequency of each unique value
    column_analysis[column] = {
        'unique_values': unique_values,
        'counts': counts
    }

# Print or save analysis
for col, analysis in column_analysis.items():
    print(f"Column: {col}")
    print(f"Unique Values: {analysis['unique_values']}")
    print(f"Counts:\n{analysis['counts'].head()}\n")

# Prepare data for unique counts bar chart
unique_counts = {col: analysis['unique_values'] for col, analysis in column_analysis.items()}

# Create subplots to display both charts in the same figure
fig, axes = plt.subplots(2, 1, figsize=(12, 14))

# Plot 1: Bar chart for unique value counts for each column
sns.barplot(x=list(unique_counts.keys()), y=list(unique_counts.values()), ax=axes[0])
axes[0].set_title("Unique Value Counts for Each Column")
axes[0].set_xlabel("Columns")
axes[0].set_ylabel("Unique Values")
axes[0].tick_params(axis='x', rotation=45)

# Plot 2: Heatmap showing missing values
sns.heatmap(df.isnull(), cbar=False, cmap="viridis", yticklabels=False, ax=axes[1])
axes[1].set_title("Missing Values Heatmap")
axes[1].set_xlabel("Columns")

# Display the plots
plt.tight_layout()
plt.show()
