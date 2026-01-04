import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from typing import List



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:

    """Reads a yaml file and returns

    Args:
        path_to_yaml (str): path like input
    
    Raises:
        valueError: if Empty yaml file
        e: Empty yaml file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list):

    """create directories

    Args:
        path_to_directories (list[Path]): list of path of directories
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logger.info(f"created directory at: {path}")



@ensure_annotations
def  get_size(path: Path) -> str:
    """get size of file

    Args:
        path (Path): path of file

    Returns:
        str: size of file in kb
    """
    size_in_kb = round(os.path.getsize(path) / 1024, 2)
    return f"~{size_in_kb} KB"   