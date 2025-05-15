# Plot-twist

**Plot-twist** is a Python tool that generates professional data visualizations from CSV files using natural language queries. It leverages Google Gemini LLM to interpret your request and automatically creates insightful matplotlib plots, along with a brief description of the visualization.

## Features

- **Natural Language Plotting:** Just describe the plot you want in plain English.
- **Automatic Data Analysis:** The system inspects your CSV and intelligently matches your request to the data.
- **Professional Visuals:** Plots are generated using matplotlib, suitable for reports and presentations.
- **Gemini LLM Integration:** Uses Google Gemini to interpret queries and generate plotting code.
- **Easy Integration:** Use as a module in your own scripts or as a standalone CLI tool.

## Installation

1. Clone the repository:
    ```sh
    git clone <your-repo-url>
    cd Plot-twist
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your `.env` file with your Gemini API key:
    ```
    GEMINI_API_KEY="your-gemini-api-key"
    ```

## Usage

### As a Python Module

```python
from plotwist import plot_from_csv

csv_file = "your_data.csv"
user_query = "Plot a scatter plot of age vs. social media addiction score"
plot_from_csv(csv_file, user_query, show_code=True)