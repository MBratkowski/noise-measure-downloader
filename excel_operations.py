import os
import re

import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from logging_util import log_info, log_warning


def create_excel_with_monthly_charts(csv_files_dict):
    for key, csv_files in csv_files_dict.items():
        parts = key.split('_')
        location, year = parts[0], parts[1]

        for csv_file in csv_files:
            match = re.search(r'monthly_average_noise_levels_(\d{4})_(\d{2})', csv_file)
            if match:
                year, month = match.groups()
                sheet_name = f"{year}_{month}_data"

                output_excel = f'output/{location}/{year}/sheets/{sheet_name}.xlsx'
                os.makedirs(os.path.dirname(output_excel), exist_ok=True)
                writer = pd.ExcelWriter(output_excel, engine='openpyxl')

                log_info(f"Creating Excel sheets for {location} in {year}-{month}")
                df = pd.read_csv(csv_file)
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

                df['LaeqD'] = df['LaeqD'].astype(float)
                df['LaeqN'] = df['LaeqN'].astype(float)
                filtered_df = df[(df['LaeqD'] != 0.0) & (df['LaeqN'] != 0.0)]

                plt.figure(figsize=(14, 7))
                plt.plot(filtered_df['Day'], filtered_df['LaeqD'], label='LaeqD', marker='o')
                plt.plot(filtered_df['Day'], filtered_df['LaeqN'], label='LaeqN', marker='o')
                plt.xlabel('Day')
                plt.title(sheet_name)
                plt.ylabel('Level (dB)')
                plt.legend()

                plt.xticks(ticks=range(1, 32), labels=[str(i) for i in range(1, 32)])

                chart_filename = f"month_{year}_{month}.png"
                chart_dir = os.path.join(os.path.dirname(output_excel), 'charts')
                os.makedirs(chart_dir, exist_ok=True)
                chart_path = os.path.join(chart_dir, chart_filename)
                plt.savefig(chart_path, bbox_inches='tight')
                plt.close()

                workbook = writer.book
                worksheet = writer.sheets[sheet_name[:31]]
                img = openpyxl.drawing.image.Image(chart_path)
                worksheet.add_image(img, 'G2')

                writer.close()
                log_info(f"Excel chart created: {output_excel}")


def create_excel_with_yearly_charts(csv_files_dict, avg_df_dict):
    for key, csv_files in csv_files_dict.items():
        parts = key.split('_')
        location, year = parts[0], parts[1]
        sheet_name = f"{year}_data"

        output_excel = f'output/{location}/{year}/sheets/year_{year}.xlsx'
        os.makedirs(os.path.dirname(output_excel), exist_ok=True)
        writer = pd.ExcelWriter(output_excel, engine='openpyxl')

        log_info(f"Creating yearly Excel sheet for {location} in {year}")
        avg_df = avg_df_dict[key]
        avg_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

        avg_df['Avg_LaeqD'] = avg_df['Avg_LaeqD'].astype(float)
        avg_df['Avg_LaeqN'] = avg_df['Avg_LaeqN'].astype(float)
        filtered_df = avg_df[(avg_df['Avg_LaeqD'] != 0.0) & (avg_df['Avg_LaeqN'] != 0.0)]

        plt.figure()
        plt.plot(filtered_df['Month'], filtered_df['Avg_LaeqD'], label='Avg_LaeqD', marker='o')
        plt.plot(filtered_df['Month'], filtered_df['Avg_LaeqN'], label='Avg_LaeqN', marker='o')
        plt.xlabel('Month')
        plt.title(f"{location} {year} Averages")
        plt.ylabel('Level (dB)')
        plt.legend()

        plt.xticks(ticks=range(1, 13),
                   labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

        chart_filename = f"year_{year}.png"
        chart_dir = os.path.join(os.path.dirname(output_excel), 'charts')
        os.makedirs(chart_dir, exist_ok=True)
        chart_path = os.path.join(chart_dir, chart_filename)
        plt.savefig(chart_path)
        plt.close()

        workbook = writer.book
        worksheet = writer.sheets[sheet_name[:31]]
        img = openpyxl.drawing.image.Image(chart_path)
        worksheet.add_image(img, 'G2')

        writer.close()
        log_info(f"Yearly Excel chart created: {output_excel}")


def create_excel_with_long_term_charts(csv_files_dict, avg_df, output_excel):
    os.makedirs(os.path.dirname(output_excel), exist_ok=True)
    writer = pd.ExcelWriter(output_excel, engine='openpyxl')

    log_info(f"Creating long term Excel charts.")
    sheet_name = "Long_Term_Avg"
    avg_df.to_excel(writer, sheet_name=sheet_name, index=False)

    avg_df['Avg_LaeqD'] = avg_df['Avg_LaeqD'].astype(float)
    avg_df['Avg_LaeqD'] = avg_df['Avg_LaeqD'].astype(float)
    filtered_df = avg_df[(avg_df['Avg_LaeqD'] != 0.0) & (avg_df['Avg_LaeqN'] != 0.0)]

    plt.figure(figsize=(20, 7))
    plt.plot(filtered_df['Date'], filtered_df['Avg_LaeqD'], label='Avg_LaeqD', marker='o')
    plt.plot(filtered_df['Date'], filtered_df['Avg_LaeqN'], label='Avg_LaeqN', marker='o')
    plt.xlabel('Month')
    plt.title(sheet_name)
    plt.ylabel('Level (dB)')
    plt.legend()

    chart_filename = "long_term.png"
    chart_dir = os.path.join(os.path.dirname(output_excel), 'charts')
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, chart_filename)
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    img = openpyxl.drawing.image.Image(chart_path)
    worksheet.add_image(img, 'G2')

    writer.close()
    log_info(f"Long-term Excel chart created: {output_excel}")
