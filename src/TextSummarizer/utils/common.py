import os
import yaml
from typing import Any
from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
from box.exceptions import BoxValueError
from TextSummarizer.logging import logger


@ensure_annotations # decorator to ensure type annotations are followed Path and return type is ConfigBox
def read_yaml(path_to_yaml: Path) -> ConfigBox:  # why ConfigBox? because it allows attribute-style access to dictionary items ex: config.key instead of config['key']
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except BoxValueError as e:
        logger.error(f"Error reading YAML file at {path_to_yaml}: {e}")
        raise
    


@ensure_annotations
def create_directories(path_to_directories: list, verbos= True):
    for path in path_to_directories:
        try:
            os.makedirs(path, exist_ok=True)
            if verbos:
                logger.info(f"Created directory at {path}")
        except Exception as e:
            logger.error(f"Error creating directory at {path}: {e}")
            raise


@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"