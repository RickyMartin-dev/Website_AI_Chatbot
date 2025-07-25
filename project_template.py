# Imports
import os
from pathlib import Path
import logging

# Define Logging Format
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# specify files to create
list_of_files = [
    ".env", # purely for local development
    ".github/workflows/.gitkeep",
    "Notebooks/testing.py", # for testing files if needed
    # "scripts/create_buckets.py", # create proper S3 buckets if need be
    "src/__init__.py", # to import files
    "src/config.py", # for config files
    "src/logging.py", # dedicated logging file
    "src/bedrock.py", # for bedrock API call Code
    "src/memory.py", # in-process memory store
    "src/chat.py", # for chat logic 
    "src/main.py", # for api
    "src/agent.py", # for Langgraph Agent Logic
    "src/utils.py", # for repeated work
    "requirements.txt", # for package information 
    "Dockerfile",
    "tests/test_chat.py",
]

# Go through list and create folders/files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # logic for directory
    if filedir != "":
        # create directory
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    # Create the files
    # check if file exists I do not want to replace
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else: # if file already exists
        logging.info(f"{filename} already exists")