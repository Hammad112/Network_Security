import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = 'NetworkSecurity'

list_of_files = [
    '.github/workflows/main.yml',
    'Network_Data/',  
    'notebooks/',  
    f'{project_name}/__init__.py',
    f'{project_name}/components/__init__.py',
    f'{project_name}/constant/__init__.py',
    f'{project_name}/entity/__init__.py',
    f'{project_name}/logging/__init__.py',
    f'{project_name}/exception/__init__.py',
    f'{project_name}/pipeline/__init__.py',
    f'{project_name}/utils/__init__.py',
    f'{project_name}/cloud/__init__.py',
    'requirements.txt',
    '.gitignore',
    'Readme.md',
    'setup.py',
    'Dockerfile'  # Ensure this is treated as a file, not a directory
]

dockerfile_content = """\
"""

for filepath in list_of_files:
    filepath = Path(filepath)

    if filepath.suffix or filepath.name in ["Dockerfile", ".gitignore", "Readme.md"]:  # Ensure Dockerfile is treated as a file
        filedir = filepath.parent
        os.makedirs(filedir, exist_ok=True)
        logging.info(f'Creating directory {filedir} for the file {filepath.name}')

        if not filepath.exists() or filepath.stat().st_size == 0:
            with open(filepath, 'w') as f:
                if filepath.name == "Dockerfile":
                    f.write(dockerfile_content)  # Write Dockerfile content
                logging.info(f'Creating file {filepath.name} at {filepath}')
    else:  # If it's a directory
        os.makedirs(filepath, exist_ok=True)
        logging.info(f'Creating directory {filepath}')
