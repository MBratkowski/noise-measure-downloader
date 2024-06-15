
# Noise Measurement Data Processor

This project processes PDF files containing noise measurement data and generates CSV and Excel files with aggregated results and charts. The project also creates consolidated CSV files with average monthly noise levels across multiple years for each measurement location.

## Project Structure

```plaintext
.
├── content
│   ├── location_1
│   │   ├── 2018
│   │   │   ├── data_01.pdf
│   │   │   ├── data_02.pdf
│   │   │   ├── ...
│   │   ├── 2019
│   │   │   ├── data_01.pdf
│   │   │   ├── data_02.pdf
│   │   │   ├── ...
│   │   └── ...
│   └── location_2
│       ├── 2018
│       │   ├── data_01.pdf
│       │   ├── ...
│       └── ...
├── output
│   ├── location_1
│   │   ├── 2018
│   │   │   ├── monthly_average_noise_levels_2018_01.csv
│   │   │   ├── yearly_average_noise_levels_2018.csv
│   │   │   ├── Noise_Levels_Charts_2018.xlsx
│   │   └── combined_average_noise_levels.csv
│   └── location_2
│       ├── ...
├── pdf_processing.py
├── csv_operations.py
├── excel_operations.py
├── main.py
└── README.md
```

## Setup and Requirements

### Prerequisites

- Python 3.6+
- `pip` (Python package installer)

### Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### Required Libraries

- `pandas`
- `matplotlib`
- `openpyxl`
- `PyPDF2`

### Installing Additional Libraries

You can install the required libraries using `pip`:

```bash
pip install pandas matplotlib openpyxl PyPDF2
```

## Usage

1. Place the PDF files containing noise measurement data in the appropriate directories under the `content` folder. The structure should follow the pattern `content/<location>/<year>/data_<month>.pdf`.

2. Run the `main.py` script to process the PDF files and generate the required CSV and Excel files:

```bash
python main.py
```

## Output

The output files are saved in the `output` directory with the following structure:

- `monthly_average_noise_levels_YYYY_MM.csv`: Monthly average noise levels for a specific month and year.
- `yearly_average_noise_levels_YYYY.csv`: Yearly average noise levels for a specific year.
- `Noise_Levels_Charts_YYYY.xlsx`: Excel file with charts for each month and the yearly averages.
- `combined_average_noise_levels.csv`: Consolidated average noise levels for each month across multiple years for a specific location.
- `long_term_monthly_average_noise_levels.csv`: Long-term average noise levels for each month across multiple locations and years.

## Functions

### PDF Processing

- `find_pdf_files(directory)`: Recursively finds all PDF files in a directory.
- `process_pdf(filepath, index, total)`: Processes a single PDF file and extracts noise level data from the relevant pages.

### CSV Operations

- `find_csv_files(directory)`: Recursively finds all CSV files in a directory.
- `save_monthly_data(data, filename)`: Saves monthly noise level data to a CSV file.
- `create_yearly_average_csv(csv_files, output_csv)`: Creates a yearly average CSV file from monthly CSV files.
- `create_long_term_average_csv(csv_files_by_location, output_csv)`: Creates a long-term average CSV file from multiple CSV files grouped by location.
- `create_combined_average_csv(csv_files, output_csv)`: Creates a consolidated average CSV file for each location with average monthly noise levels across multiple years.

### Excel Operations

- `create_excel_with_charts(csv_files, avg_df, output_excel)`: Creates an Excel file with charts for each month and the yearly averages.

## Logging

The script logs progress to the console, indicating which PDF file is being processed and where the CSV and Excel files are being saved.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgements

This project was created with the help of the following libraries:

- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [PyPDF2](https://pythonhosted.org/PyPDF2/)
