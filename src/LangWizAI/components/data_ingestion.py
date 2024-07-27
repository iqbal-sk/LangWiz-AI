import os
import requests
import gzip
import shutil
import pandas as pd

from LangWizAI import logger
from LangWizAI.entity.config_entity import EuroparlDataIngestionConfig


class DataIngestion:
    def __init__(self, config: EuroparlDataIngestionConfig):
        self.config = config

        # Create directories if they don't exist
        os.makedirs(self.config.root_dir, exist_ok=True)
        os.makedirs(self.config.unzip_dir, exist_ok=True)

    def download_and_extract(self, dataset):
        # Download dataset
        file_url = self.config.source_URL + dataset
        local_gz_path = os.path.join(self.config.root_dir, dataset)
        logger.info(f"Downloading {dataset} in {local_gz_path}")
        response = requests.get(file_url, stream=True)
        with open(local_gz_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        # Extract dataset
        local_tsv_path = local_gz_path[:-3]  # Remove .gz extension
        logger.info(f"Extracting {dataset} to {local_tsv_path}")
        with gzip.open(local_gz_path, 'rb') as f_in:
            with open(local_tsv_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Process TSV file
        self.process_tsv(local_tsv_path)

    def process_tsv(self, tsv_path):
        logger.info(f"Processing {tsv_path}...")
        try:
            df = pd.read_csv(tsv_path, sep='\t', header=None, usecols=[0, 1],
                             names=['source_text', 'target_text'])
        except Exception as e:
            print(f"Error processing {tsv_path}: {e}")
            return
        # Get source and target language from file name
        base_name = os.path.basename(tsv_path)

        source_lang, target_lang = base_name.split('-')[1].split('.')[1], base_name.split('-')[2].split('.')[0]

        # Create directories for source and target languages
        source_dir = os.path.join(self.config.unzip_dir, f"{source_lang}_{target_lang}")
        os.makedirs(source_dir, exist_ok=True)

        # Save processed TSV
        processed_tsv_path = os.path.join(source_dir, f"{source_lang}_{target_lang}.csv")

        columns = ['source_text', 'target_text']

        for column in columns:
            df = df[df[column].notna()]  # Remove rows with missing values
            df = df[df[column].str.strip() != '']

        df[['source_text', 'target_text']].to_csv(processed_tsv_path, sep=',', index=False)
        logger.info(f"Saved processed TSV to {processed_tsv_path}")


    def download_and_process(self):
        for dataset in self.config.dataset_names:
            self.download_and_extract(dataset)



