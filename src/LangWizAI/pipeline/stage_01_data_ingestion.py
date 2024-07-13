import os

from LangWizAI.config.configuration import ConfigurationManager
from LangWizAI.components.data_ingestion import DataIngestion
from LangWizAI import logger



STAGE_NAME = "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        euro_data_ingestion_config = config.get_euro_data_ingestion_config()
        data_ingestion = DataIngestion(config=euro_data_ingestion_config)
        data_ingestion.download_and_process()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

