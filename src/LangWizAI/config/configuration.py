import os
from LangWizAI.constants import *
from LangWizAI.utils.common import read_yaml, create_directories
from LangWizAI.entity.config_entity import EuroparlDataIngestionConfig


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH):

        self.config = read_yaml(config_filepath)

        create_directories([self.config.artifacts_root])

    def get_euro_data_ingestion_config(self) -> EuroparlDataIngestionConfig:
        config = self.config.europarl_data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = EuroparlDataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            unzip_dir=config.unzip_dir,
            dataset_names=config.dataset_names
        )

        return data_ingestion_config