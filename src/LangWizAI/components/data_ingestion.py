import os
import requests
import gzip
import shutil
import pandas as pd

from LangWizAI import logger
from LangWizAI.entity.config_entity import EuroparlDataIngestionConfig, WMTChatDataIngestionConfig


class DataIngestion:
    def __init__(self, config: EuroparlDataIngestionConfig,
                 wmt_config: WMTChatDataIngestionConfig):
        self.config = config
        self.wmt_config = wmt_config

        # Create directories if they don't exist
        os.makedirs(self.config.root_dir, exist_ok=True)
        os.makedirs(self.config.unzip_dir, exist_ok=True)
        os.makedirs(self.wmt_config.root_dir, exist_ok=True)
        os.makedirs(self.wmt_config.unzip_dir, exist_ok=True)

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

    def download_and_process_europarl(self):
        for dataset in self.config.dataset_names:
            self.download_and_extract(dataset)

    def download_and_extract_wmt_chat(self, dataset):
        # Download additional dataset
        file_url = self.wmt_config.source_URL + dataset
        local_csv_path = os.path.join(self.wmt_config.root_dir, dataset)
        logger.info(f"Downloading {dataset} to {local_csv_path}")
        response = requests.get(file_url, stream=True)
        with open(local_csv_path, 'wb') as f:
            f.write(response.content)

        # Process CSV file
        self.process_wmt_chat_csv(local_csv_path, dataset)

    def process_wmt_chat_csv(self, csv_path, dataset):
        logger.info(f"Processing {csv_path}...")
        try:
            df = pd.read_csv(csv_path)
            df = df[['source', 'reference']]
            df.rename(columns={'source': 'source_text', 'reference': 'target_text'}, inplace=True)

            columns = ['source_text', 'target_text']

            for column in columns:
                df = df[df[column].notna()]  # Remove rows with missing values
                df = df[df[column].str.strip() != '']

        except Exception as e:
            logger.error(f"Error processing {csv_path}: {e}")
            return

        # Create directories for the processed CSV
        base_name = os.path.basename(dataset)
        lang_pair_dir = os.path.join(self.wmt_config.unzip_dir, os.path.dirname(dataset))
        os.makedirs(lang_pair_dir, exist_ok=True)

        # Save processed CSV
        processed_csv_path = os.path.join(lang_pair_dir, base_name)
        df.to_csv(processed_csv_path, index=False)
        logger.info(f"Saved processed CSV to {processed_csv_path}")

    def download_and_process_wmt_chat(self):
        train_dir = os.path.join(self.wmt_config.root_dir, 'train')
        val_dir = os.path.join(self.wmt_config.root_dir, 'valid')

        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

        for dataset in self.wmt_config.dataset_names:
            self.download_and_extract_wmt_chat(dataset)

    def download_and_process(self):
        # self.download_and_process_europarl()
        self.download_and_process_wmt_chat()



