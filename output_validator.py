import os
import re
from colorama import init, Fore, Style

init(autoreset=True)


def validate_files(base_directory):
    def check_files_in_dir(path, file_pattern, expected_count, description):
        if not os.path.exists(path):
            print(f"{Fore.RED}✗ Directory not found: {path}")
            return False
        files = [f for f in os.listdir(path) if file_pattern.match(f)]
        if len(files) == expected_count:
            print(f"{Fore.GREEN}✓ Found {expected_count} {description}")
        else:
            print(f"{Fore.RED}✗ Expected {expected_count} {description}, found {len(files)}")
        return len(files) == expected_count

    for point in os.listdir(base_directory):
        point_path = os.path.join(base_directory, point)
        if os.path.isdir(point_path):
            for year in os.listdir(point_path):
                year_path = os.path.join(point_path, year)
                if os.path.isdir(year_path):
                    csv_path = os.path.join(year_path, 'csv')
                    sheets_path = os.path.join(year_path, 'sheets')
                    charts_path = os.path.join(sheets_path, 'charts')

                    if os.path.exists(csv_path):
                        print(f"{Fore.BLUE}Validating CSV files in directory: {csv_path}")

                        monthly_pattern = re.compile(r'monthly_average_noise_levels_\d{4}_(\d{2})\.csv')
                        yearly_pattern = re.compile(r'yearly_average_noise_levels_\d{4}\.csv')

                        monthly_csv_files = [f for f in os.listdir(csv_path) if monthly_pattern.match(f)]
                        yearly_csv_files = [f for f in os.listdir(csv_path) if yearly_pattern.match(f)]

                        current_year = int(year)
                        current_month = len(monthly_csv_files)

                        # For current year, we might not have all 12 months yet
                        if current_year == 2024 and current_month <= 12:
                            valid_monthly_csv = True
                            print(
                                f"{Fore.YELLOW}~ Found {current_month} monthly CSV files for incomplete year {current_year}")
                        else:
                            valid_monthly_csv = check_files_in_dir(csv_path, monthly_pattern, 12, 'monthly CSV files')

                        valid_yearly_csv = check_files_in_dir(csv_path, yearly_pattern, 1, 'yearly CSV file')

                        if not (valid_monthly_csv and valid_yearly_csv):
                            print(f"{Fore.RED}✗ CSV validation failed in {csv_path}")

                        if os.path.exists(sheets_path):
                            print(f"{Fore.BLUE}Validating Excel files in directory: {sheets_path}")

                            monthly_excel_pattern = re.compile(r'\d{4}_\d{2}_data\.xlsx')
                            yearly_excel_pattern = re.compile(r'year_\d{4}\.xlsx')
                            charts_pattern = re.compile(r'month_\d{4}_\d{2}\.png|year_\d{4}\.png')

                            monthly_excel_files = [f for f in os.listdir(sheets_path) if monthly_excel_pattern.match(f)]

                            # For current year, we might not have all 12 months yet
                            if current_year == 2024 and len(monthly_excel_files) <= 12:
                                valid_monthly_excel = True
                                print(
                                    f"{Fore.YELLOW}~ Found {len(monthly_excel_files)} monthly Excel files for incomplete year {current_year}")
                            else:
                                valid_monthly_excel = check_files_in_dir(sheets_path, monthly_excel_pattern, 12,
                                                                         'monthly Excel files')

                            valid_yearly_excel = check_files_in_dir(sheets_path, yearly_excel_pattern, 1,
                                                                    'yearly Excel file')

                            if os.path.exists(charts_path):
                                print(f"{Fore.BLUE}Validating chart files in directory: {charts_path}")
                                if current_year == 2024:
                                    expected_charts = current_month + 1  # number of monthly charts + 1 yearly chart
                                else:
                                    expected_charts = 13  # 12 months + 1 year

                                valid_charts = check_files_in_dir(charts_path, charts_pattern, expected_charts,
                                                                  'chart files')

                                if not valid_charts:
                                    print(f"{Fore.RED}✗ Charts validation failed in {charts_path}")
                            else:
                                print(f"{Fore.RED}✗ No charts directory found in {sheets_path}")
                        else:
                            print(f"{Fore.RED}✗ No sheets directory found in {year_path}")
                    else:
                        print(f"{Fore.RED}✗ No CSV directory found in {year_path}")

            # Validate long term files in the base directory of the point
            long_term_csv_path = os.path.join(point_path, 'csv', f'{point}_long_term_monthly_average_noise_levels.csv')
            long_term_excel_path = os.path.join(point_path, 'sheets',
                                                f'{point}_long_term_monthly_average_noise_levels.xlsx')
            long_term_chart_path = os.path.join(point_path, 'sheets', 'charts', 'long_term.png')

            if os.path.exists(long_term_csv_path):
                print(f"{Fore.BLUE}Validating long term CSV file: {long_term_csv_path}")
                print(f"{Fore.GREEN}✓ Found long term CSV file: {long_term_csv_path}")
            else:
                print(f"{Fore.RED}✗ Long term CSV file not found: {long_term_csv_path}")

            if os.path.exists(long_term_excel_path):
                print(f"{Fore.BLUE}Validating long term Excel file: {long_term_excel_path}")
                print(f"{Fore.GREEN}✓ Found long term Excel file: {long_term_excel_path}")
            else:
                print(f"{Fore.RED}✗ Long term Excel file not found: {long_term_excel_path}")

            if os.path.exists(long_term_chart_path):
                print(f"{Fore.BLUE}Validating long term chart file: {long_term_chart_path}")
                print(f"{Fore.GREEN}✓ Found long term chart file: {long_term_chart_path}")
            else:
                print(f"{Fore.RED}✗ Long term chart file not found: {long_term_chart_path}")


if __name__ == "__main__":
    base_directory = 'output'
    validate_files(base_directory)
