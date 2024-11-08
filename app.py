import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3

# Load CSV
df = pd.read_csv("FieldValuesExport_MultipleFiles.csv")

# Analyze unique values and counts for each column
column_analysis = {}
for column in df.columns:
    unique_values = df[column].nunique()  # Number of unique values
    counts = df[column].value_counts()    # Frequency of each unique value
    column_analysis[column] = {
        'unique_values': unique_values,
        'counts': counts
    }

# Prepare data for unique counts bar chart
unique_counts = {col: analysis['unique_values'] for col, analysis in column_analysis.items()}

# Identify columns with more than one unique value and prepare data
columns_with_multiple_unique = [col for col, count in unique_counts.items() if count > 1]
multiple_unique_counts = {col: unique_counts[col] for col in columns_with_multiple_unique}

# Create a figure with 3 subplots
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

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

# Plot 3: Bar chart for columns with more than one unique value
sns.barplot(x=list(multiple_unique_counts.keys()), y=list(multiple_unique_counts.values()), ax=axes[2])
axes[2].set_title("Unique Value Counts for Columns with More than One Unique Value")
axes[2].set_xlabel("Columns")
axes[2].set_ylabel("Unique Values")
axes[2].tick_params(axis='x', rotation=45)

# Adjust layout for clarity
plt.tight_layout()

# Export to HTML
html_str = mpld3.fig_to_html(fig)
with open("plots.html", "w") as f:
    f.write(html_str)

plt.show()
