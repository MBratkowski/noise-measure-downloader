import os
import re
import pandas as pd
from logging_util import log_info, log_warning


def save_monthly_data(data, filename):
    df = pd.DataFrame(data, columns=["Day", "LaeqD", "LaeqN"])
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    log_info(f"Saved data for {filename}")


def create_yearly_average_csv(csv_files, output_csv):
    all_averages = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)

        if "Day" in df.columns:
            avg_laeqd = df["LaeqD"].mean()
            avg_laeqn = df["LaeqN"].mean()
        else:
            avg_laeqd = df["Avg_LaeqD"].mean()
            avg_laeqn = df["Avg_LaeqN"].mean()

        match = re.search(r'monthly_average_noise_levels_\d{4}_(\d{2})', csv_file)
        if match:
            month = match.group(1)
            all_averages.append([f"{month}", avg_laeqd, avg_laeqn])

    avg_df = pd.DataFrame(all_averages, columns=["Month", "Avg_LaeqD", "Avg_LaeqN"])
    avg_df = avg_df.sort_values(by="Month")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    avg_df.to_csv(output_csv, index=False)
    log_info(f"Yearly average CSV created: {output_csv}")
    return avg_df


def create_long_term_average_csv(csv_files_dict, output_csv):
    all_data = []

    for key, csv_files in csv_files_dict.items():
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df['Month'] = re.search(r'monthly_average_noise_levels_\d{4}_(\d{2})', csv_file).group(1)
            df['Year'] = re.search(r'(\d{4})', csv_file).group(1)
            df['Date'] = df['Year'] + '-' + df['Month']
            all_data.append(df)

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df[['Date', 'LaeqD', 'LaeqN']]
        combined_df = combined_df.groupby('Date').mean().reset_index()
        combined_df.rename(columns={'LaeqD': 'Avg_LaeqD'}, inplace=True)
        combined_df.rename(columns={'LaeqN': 'Avg_LaeqN'}, inplace=True)
        combined_df.sort_values(by='Date', inplace=True)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        combined_df.to_csv(output_csv, index=False)
        log_info(f"Long term average CSV created: {output_csv}")
        return combined_df
    else:
        log_warning("No data available to concatenate.")
        return None


def find_csv_files(directory):
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files
