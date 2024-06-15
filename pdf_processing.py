import os
import re

import PyPDF2
from logging_util import log_info, log_error, log_warning


def find_pdf_files(directory):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def extract_table_from_text(text):
    lines = text.split('\n')
    table_data = []
    capture = False

    for line in lines:
        line = line.strip()
        if capture:
            match = re.match(r'^\d{1,2}\s+\d{1,2},\d\s+\d{1,2},\d$', line)
            if match:
                parts = re.split(r'\s+', line)
                day, laeqd, laeqn = parts[0], parts[1], parts[2]
                table_data.append([day, laeqd.replace(',', '.'), laeqn.replace(',', '.')])
            else:
                continue
        elif re.match(r'^1\s+\d{1,2},\d\s+\d{1,2},\d$', line):
            capture = True
            parts = re.split(r'\s+', line)
            day, laeqd, laeqn = parts[0], parts[1], parts[2]
            table_data.append([day, laeqd.replace(',', '.'), laeqn.replace(',', '.')])

    return table_data


def process_pdf(filepath, index, total):
    log_info(f"Processing file {index + 1}/{total}: {filepath}")
    with open(filepath, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)

        start_page = 0
        end_page = num_pages - 1

        expected_phrases = [
            "Równoważny poziom dźwięku w porze dnia i w porze nocy",
            "Równoważny poziom dźwięku",
            "Równoważny poziom d źwięku",
            "Dzień miesiąca"
        ]

        while start_page <= end_page:
            for page_num in [start_page, end_page]:
                page = pdf_reader.pages[page_num]
                text = page.extract_text().strip()  # Strip leading and trailing whitespace
                log_info(f"Processing PDF {index + 1}/{total} - page {page_num + 1}/{num_pages}")

                # Check for any of the expected phrases using 'in'
                if any(phrase in text for phrase in expected_phrases):
                    table_data = extract_table_from_text(text)
                    if table_data:
                        return table_data

            start_page += 1
            end_page -= 1

    return []
