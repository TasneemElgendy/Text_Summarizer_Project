import os
import urllib.request as request
import zipfile
from TextSummarizer.utils.common import get_size
from TextSummarizer.logging import logger
from TextSummarizer.entity import (DataIngestionConfig)
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers =  request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
    
    
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            logger.info(f"Extracting zip file :[{self.config.local_data_file}] into dir :[{unzip_path}]")
            zip_ref.extractall(unzip_path)
            logger.info(f"Extraction completed successfully.")
            
        
        # if os.path.exists(unzip_path):
        #     logger.info(f"Unzip directory :[{unzip_path}] already exists. Hence removing it first.")
        #     os.remove(unzip_path)
        