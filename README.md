# PyWebIO Data Analysis with Plotly

This project is a web application for visual data analysis of CSV files. It uses PyWebIO for the user interface and Plotly for generating visualizations. Users can upload CSV files, view data summaries, and analyze unique values, missing values, and categorical distributions with interactive charts.


![alt text](assests/di.webp "Title-1")


## Features

- **File Upload**: Upload any CSV file for analysis.
- **Unique Value Analysis**: Displays a bar chart for unique value counts across columns.
- **Missing Data Heatmap**: Visualizes missing values in the data using a heatmap.
- **Customizable Donut Charts**: Creates donut charts for columns with 2 to 5 unique values, displayed in rows of three.

## Installation

To run this project, you'll need Python 3.7+ and the following libraries:

```bash
pip install pywebio plotly pandas
```

## Usage

1. **Start the Server**: Run the application with the following command:
   ```bash
   python web.py
   ```

2. **Upload a CSV File**: Go to `http://localhost:8080`, upload your CSV file, and view analysis results.

### Example Visualizations

1. **Unique Value Counts for Each Column**: Displays a bar chart showing the unique value counts for each column in the dataset.
2. **Missing Values Heatmap**: A heatmap indicating the presence of missing values across rows and columns.
3. **Donut Charts**: For columns with 2-5 unique values, interactive donut charts display the distribution of each unique value.

---

### Example Usage

For testing purposes, try uploading a sample CSV file to explore the visualizations.

--- 

### License

This project is licensed under the MIT License.