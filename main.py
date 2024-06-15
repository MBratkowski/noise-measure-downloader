import os
import re
from pdf_processing import find_pdf_files, process_pdf
from csv_operations import save_monthly_data, create_yearly_average_csv, find_csv_files, create_long_term_average_csv
from excel_operations import create_excel_with_monthly_charts, create_excel_with_yearly_charts, \
    create_excel_with_long_term_charts
from logging_util import log_info, log_warning, log_error


def main():
    output_dir = 'output'
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    pdf_directory = 'content'
    pdf_files = find_pdf_files(pdf_directory)
    total_pdfs = len(pdf_files)
    monthly_data = {}

    for index, pdf_file in enumerate(pdf_files):
        table_data = process_pdf(pdf_file, index, total_pdfs)
        if table_data:
            match = re.search(r'content/([^/]+)/(\d{4})/data_(\d{2})', pdf_file)
            if match:
                location, year, month = match.groups()
                key = f"{location}_{year}_{month}"
                if key not in monthly_data:
                    monthly_data[key] = []
                monthly_data[key].extend(table_data)
            else:
                log_warning(f"Pattern not found in {pdf_file}")

    log_info(f"Monthly data collected: {monthly_data.keys()}")

    csv_files_dict = {}
    for key, data in monthly_data.items():
        parts = key.split('_')
        if len(parts) == 3:
            location, year, month = parts
            output_dir = f'output/{location}/{year}/csv'
            filename = os.path.join(output_dir, f"monthly_average_noise_levels_{year}_{month}.csv")
            save_monthly_data(data, filename)
            if f"{location}_{year}" not in csv_files_dict:
                csv_files_dict[f"{location}_{year}"] = []
            csv_files_dict[f"{location}_{year}"].append(filename)
        else:
            log_warning(f"Unexpected key format: {key}")

    log_info(f"Monthly CSV files created: {monthly_data.keys()}")

    yearly_csv_files_dict = {}
    avg_df_dict = {}
    for key, csv_files in csv_files_dict.items():
        parts = key.split('_')
        location, year = parts[0], parts[1]
        output_dir = f'output/{location}/{year}/csv'
        yearly_csv_path = os.path.join(output_dir, f'yearly_average_noise_levels_{year}.csv')
        avg_df = create_yearly_average_csv(csv_files, yearly_csv_path)
        log_info(f"Yearly average CSV created: {yearly_csv_path}")
        yearly_csv_files_dict[key] = csv_files
        avg_df_dict[key] = avg_df

    create_excel_with_monthly_charts(csv_files_dict)
    create_excel_with_yearly_charts(yearly_csv_files_dict, avg_df_dict)

    csv_directory = 'output'
    csv_files = find_csv_files(csv_directory)
    csv_files_by_location = {}

    for csv_file in csv_files:
        match = re.search(r'output/([^/]+)/(\d{4})/csv/monthly_average_noise_levels_\d{4}_\d{2}\.csv', csv_file)
        if match:
            location = match.groups()[0]
            if location not in csv_files_by_location:
                csv_files_by_location[location] = []
            csv_files_by_location[location].append(csv_file)

    log_info(f"CSV files by location: {csv_files_by_location.keys()}")

    for location, files in csv_files_by_location.items():
        long_term_avg_csv_path = f'output/{location}/csv/{location}_long_term_monthly_average_noise_levels.csv'
        avg_df = create_long_term_average_csv({location: files}, long_term_avg_csv_path)

        if avg_df is not None:
            long_term_excel_path = f'output/{location}/sheets/{location}_long_term_monthly_average_noise_levels.xlsx'
            create_excel_with_long_term_charts({location: files}, avg_df, long_term_excel_path)


if __name__ == "__main__":
    main()
