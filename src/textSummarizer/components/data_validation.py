

import os
from textSummarizer.entity import DataValidationConfig
from textSummarizer.logging import logger



class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
    
    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None
            all_files = os.listdir(self.config.data_path)


            for file in all_files:
                if file not in self.config.ALL_REQUIRED_FILES:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"validation_status: {validation_status}\n")

                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"validation_status: {validation_status}\n")
           
            return validation_status
        except Exception as e:
            raise e
                