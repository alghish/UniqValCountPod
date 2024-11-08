import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pywebio.output import put_html, put_text, put_markdown
from pywebio import start_server

from pywebio.input import file_upload
import io



# Function to display plots in PyWebIO
def display_plots():
    # CSV
    # Load CSV
    # File upload widget
    uploaded_file = file_upload("Upload your CSV file", accept="text/csv")
    
    # Convert the uploaded file into a pandas DataFrame using io.BytesIO
    file_content = uploaded_file['content']
    file_stream = io.BytesIO(file_content)
    df = pd.read_csv(file_stream)
    # df = pd.read_csv("FieldValuesExport_MultipleFiles.csv")

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
    unique_counts_df = pd.DataFrame(list(unique_counts.items()), columns=['Column', 'Unique Values'])

    # Identify columns with more than one unique value and prepare data
    columns_with_multiple_unique = [col for col, count in unique_counts.items() if count > 1]
    multiple_unique_counts_df = unique_counts_df[unique_counts_df['Column'].isin(columns_with_multiple_unique)]

    # Plot 1: Unique value counts for each column
    fig1 = px.bar(unique_counts_df, x='Column', y='Unique Values', title="Unique Value Counts for Each Column")
    fig1.update_layout(xaxis_tickangle=-45)

    # ///
    # Plot 2: Heatmap for missing values using plotly.express
    # We use `.isnull()` to create a boolean matrix (True for NaN), which is then converted to integers (1 for NaN, 0 otherwise)
    missing_data = df.isnull().astype(int)
    fig2 = px.imshow(missing_data, color_continuous_scale='Viridis', aspect='auto')
    fig2.update_layout(title="Missing Values Heatmap", xaxis_title="Columns", yaxis_title="Rows")
    # ///

    # Plot 3: Unique value counts for columns with more than one unique value
    fig3 = px.bar(multiple_unique_counts_df, x='Column', y='Unique Values', title="Unique Value Counts for Columns with More than One Unique Value")
    fig3.update_layout(xaxis_tickangle=-45)

    # Adding a title to the page to ensure it loads
    put_markdown("# Data Analysis with Plotly and PyWebIO")
    
    # Adding descriptions to check if page is rendered
    put_text("Below are the visualizations for unique value counts and missing data heatmap.")
    
    # Displaying each plot
    put_html(fig1.to_html(include_plotlyjs="require", full_html=False))
    put_markdown("## Missing Values Heatmap")
    put_html(fig2.to_html(include_plotlyjs="require", full_html=False))
    put_markdown("## Columns with More Than One Unique Value")
    put_html(fig3.to_html(include_plotlyjs="require", full_html=False))

# Start PyWebIO server
if __name__ == '__main__':
    start_server(display_plots, port=8080)
