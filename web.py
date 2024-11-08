import pandas as pd
import plotly.express as px
from pywebio.output import put_html, put_text, put_markdown, put_table, use_scope, popup, put_buttons, put_row, put_processbar, set_processbar
from pywebio import start_server
from pywebio.input import file_upload
import io

# Function to display plots in PyWebIO
def display_plots():
    # File upload widget
    uploaded_file = file_upload("Upload your CSV file", accept="text/csv")
    
    # Convert the uploaded file into a pandas DataFrame using io.BytesIO
    file_content = uploaded_file['content']
    file_stream = io.BytesIO(file_content)
    df = pd.read_csv(file_stream)

    # Display the progress bar
    num_columns = len(df.columns)
    put_processbar('progress')
    
    # Analyze unique values and counts for each column
    column_analysis = {}
    for i, column in enumerate(df.columns, start=1):
        unique_values = df[column].nunique()  # Number of unique values
        counts = df[column].value_counts()    # Frequency of each unique value
        column_analysis[column] = {
            'unique_values': unique_values,
            'counts': counts
        }
        set_processbar('progress', i / num_columns)  # Update progress bar

    # Prepare data for unique counts bar chart
    unique_counts = {col: analysis['unique_values'] for col, analysis in column_analysis.items()}
    unique_counts_df = pd.DataFrame(list(unique_counts.items()), columns=['Column', 'Unique Values'])

    # Identify columns with more than one unique value and prepare data
    columns_with_multiple_unique = [col for col, count in unique_counts.items() if count > 1]
    multiple_unique_counts_df = unique_counts_df[unique_counts_df['Column'].isin(columns_with_multiple_unique)]

    # Plot 1: Unique value counts for each column
    fig1 = px.bar(unique_counts_df, x='Column', y='Unique Values', title="Unique Value Counts for Each Column")
    fig1.update_layout(xaxis_tickangle=-45)

    # Plot 2: Heatmap for missing values using plotly.express
    missing_data = df.isnull().astype(int)
    fig2 = px.imshow(missing_data, color_continuous_scale='Viridis', aspect='auto')
    fig2.update_layout(title="Missing Values Heatmap", xaxis_title="Columns", yaxis_title="Rows")

    # Plot 3: Unique value counts for columns with more than one unique value
    fig3 = px.bar(multiple_unique_counts_df, x='Column', y='Unique Values', title="Unique Value Counts for Columns with More than One Unique Value")
    fig3.update_layout(xaxis_tickangle=-45)

    # Adding a title to the page to ensure it loads
    put_markdown("# Data Analysis with Plotly and PyWebIO")
    
    # Adding descriptions to check if page is rendered
    put_text("Below are the visualizations for unique value counts and missing data heatmap.")
    
    # Show a preview of the uploaded CSV table
    # put_markdown("### Table Preview")
    # put_html(df.head().to_html(index=False))  # Show the first few rows of the CSV as a table
    
    # # Create a list of rows with column names and the unique value counts
    # table_data = [["Column Name", "Unique Values"]]
    # for column, analysis in column_analysis.items():
    #     table_data.append([column, analysis['unique_values']])
    
    # # Display the table with column names and unique value counts
    # put_table(table_data)

        # Display "Columns Analyzed" in a collapsible section
    def show_columns_analyzed():
        # Create table data
        table_data = [["Column Name", "Unique Values"]]
        for column, analysis in column_analysis.items():
            table_data.append([column, analysis['unique_values']])
        
        # Show table in a popup when requested
        popup("Columns Analyzed", [
            put_table(table_data),
            put_buttons(['Close'], onclick=lambda _: popup.close())
        ])

    # Display each plot with column names
    put_markdown("### Plot 1: Unique Value Counts for Each Column")
    # Button to toggle the display of "Columns Analyzed"
    put_markdown("### Columns Analyzed")
    put_buttons(["Show Columns Analyzed"], onclick=lambda _: show_columns_analyzed())
    put_html(fig1.to_html(include_plotlyjs="require", full_html=False))

    put_markdown("## Plot 2: Missing Values Heatmap")
    put_html(fig2.to_html(include_plotlyjs="require", full_html=False))


    put_markdown("## Plot 3: Columns with More Than One Unique Value")

    def show_multiple_unique_counts_df():
        table_data = [multiple_unique_counts_df.columns.tolist()]  # Start with the headers
        table_data.extend(multiple_unique_counts_df.values.tolist())  # Add the rows

        # Show table in a popup when requested
        popup("Columns Analyzed", [
            put_table(table_data),
            put_buttons(['Close'], onclick=lambda _: popup.close())
        ])

    put_buttons(["Show Columns Analyzed"], onclick=lambda _: show_multiple_unique_counts_df())
    # put_text(f"Columns analyzed: {', '.join(multiple_unique_counts_df['Column'].tolist())}")  # Columns with >1 unique value
    put_html(fig3.to_html(include_plotlyjs="require", full_html=False))

    # Find columns with unique values between 2 and 5 and create donut charts
    put_markdown("## Donut Charts for Columns with 2 to 5 Unique Values")
    donut_charts = []
    count = 0

    for column, analysis in column_analysis.items():
        unique_count = analysis['unique_values']
        
        if 2 <= unique_count <= 5:
            # Create a donut chart for the column
            fig_donut = px.pie(df, names=column, hole=0.4, title=f"Donut Chart for '{column}'")
            fig_donut.update_traces(textinfo='percent+label')
            donut_charts.append(put_html(fig_donut.to_html(include_plotlyjs="require", full_html=False)))
            count += 1

            # Display the charts in rows of 3
            if count % 2 == 0:
                put_row(donut_charts)
                donut_charts = []

    # Display any remaining charts in the last row
    if donut_charts:
        put_row(donut_charts)


# Start PyWebIO server
if __name__ == '__main__':
    start_server(display_plots, port=8080)
