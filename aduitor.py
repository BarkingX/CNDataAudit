import csv
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import glob


def analyze_file(file_path):
    try:
        # Load the file
        df = pd.read_csv(file_path, quoting=csv.QUOTE_ALL)

        # Check if the DataFrame has only header row
        if df.empty or len(df) == 1:  # Only header or one data row
            return {
                'file': file_path,
                'dirty_data_ratio': 1.0,
                'completeness': 0,
                'timeliness': None,
                'description': 'Minimal content, likely only headers'
            }

        # If the file has sufficient size and more than one row, proceed with other checks
        dirty_data_count = df.isnull().any(axis=1).sum()
        total_rows = len(df)
        dirty_data_ratio = dirty_data_count / total_rows
        completeness = 1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))

        # Timeliness check, assuming a 'date' column exists
        timeliness = None
        if 'date' in df.columns:
            latest_date = pd.to_datetime(df['date']).max()
            timeliness = (pd.Timestamp.now() - latest_date).days

        return {
            'file': file_path,
            'dirty_data_ratio': dirty_data_ratio,
            'completeness': completeness,
            'timeliness': timeliness,
            'description': 'Data analyzed for quality'
        }
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e),
            'description': 'Error processing file'
        }


# Using ProcessPoolExecutor to handle the files in parallel
def main():
    path = 'sichuan/*.csv'
    files = glob.glob(path)
    results = []

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(analyze_file, files))

    # Process results here (e.g., aggregating results, printing, storing to a file, etc.)
    print(results)


if __name__ == "__main__":
    dtype = {'name': str, 'id': str, 'URL': str, 'owner': str, 'category': 'category',
             'published': 'datetime64[ns]', 'updated': 'datetime64[ns]',
             'frequency': 'category', 'sample_data': object}

    path = 'D:\Data\workspace\python\projects\CNDataAuditOutput\sichuan\dataset_catalog.json'
    df = pd.read_json(path, dtype=dtype)

    print(df.info())
    print(df.head())
