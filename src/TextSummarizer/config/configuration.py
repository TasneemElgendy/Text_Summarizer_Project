from TextSummarizer.constants import *
from TextSummarizer.utils.common import read_yaml, create_directories
from TextSummarizer.entity import (DataIngestionConfig, DataValidationConfig)

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath) #the output : ConfigBox({'artifacts_root': 'artifacts'
        # ,'data_ingestion': {'root_dir': 'artifacts/data_ingestion', 'source_URL': 'https://github.com/entbappy/Branching-tutorial/raw/master/samsumdata.zip'
        # , 'local_data_file': 'artifacts/data_ingestion/data.zip', 'unzip_dir': 'artifacts/data_ingestion'}})
        
        self.params = read_yaml(params_filepath)
        
        create_directories([self.config.artifacts_root]) 
        
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = Path(config.root_dir),
            source_URL = config.source_URL,
            local_data_file = Path(config.local_data_file),
            unzip_dir = Path(config.unzip_dir)
        )
        
        return data_ingestion_config    
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        create_directories([config.root_dir])
        data_validation_config = DataValidationConfig(
            root_dir = Path(config.root_dir),
            STATUS_FILE = config.STATUS_FILE,
            ALL_REQUIRED_FILES = config.ALL_REQUIRED_FILES
        )
        return data_validation_config

