import os
import glob
import sys
from pprint import pprint
import re
import json
import shutil

def delete_folder(path):
    # Check if the folder exists
    if os.path.exists(path):
        # Remove the folder and its contents
        shutil.rmtree(path)
        print(f"The folder at {path} has been deleted.")
    else:
        print("The specified folder does not exist.")

def select_infra_file() -> str:
    infra_files = find_files("./", "*.json")
    if not infra_files:
        print("No infra files were found in the current directory\n")
        sys.exit(1)
    selected_infra_file = input(f"Select one infra file {infra_files}: ")
    
    if not (selected_infra_file in infra_files):
        print("Select a valid infra file")
        return ""
    
    return selected_infra_file

def add_text_to_file(original_file_path, new_file_path, text):
    """
    Add text to a file and save it to another path.
    
    Args:
        original_file_path (str): The path to the original file.
        new_file_path (str): The path to save the modified file.
        text (str): The text to be added.
        
    Returns:
        bool: True if the text was successfully added and saved, False otherwise.
    """
    try:
        with open(original_file_path, 'r') as original_file:
            original_contents = original_file.read()

        with open(new_file_path, 'w') as new_file:
            new_file.write(original_contents)
            new_file.write(text)
            print(f"Text added to '{original_file_path}' and saved to '{new_file_path}' successfully.")
            return True
    except FileNotFoundError:
        print(f"Error: File '{original_file_path}' not found.")
        return False
    except Exception as e:
        print(f"Error: Failed to add text to '{original_file_path}' and save to '{new_file_path}'. {e}")
        return False

def copy_file(source_file, destination_directory):
    """
    Copy a file to another directory.
    
    Args:
        source_file (str): The path to the source file.
        destination_directory (str): The path to the destination directory.
        
    Returns:
        bool: True if the file was successfully copied, False otherwise.
    """
    try:
        shutil.copy(source_file, destination_directory)
        print(f"File '{source_file}' copied to '{destination_directory}' successfully.")
        return True
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
        return False
    except PermissionError:
        print(f"Error: Permission denied. Cannot copy file '{source_file}'.")
        return False
    except Exception as e:
        print(f"Error: Failed to copy file '{source_file}'. {e}")
        return False

def create_directory(directory_path):
    """
    Create a directory.
    
    Args:
        directory_path (str): The path to the directory to be created.
        
    Returns:
        bool: True if the directory was successfully created, False otherwise.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory '{directory_path}' created successfully.")
        return True
    except OSError as e:
        print(f"Error: Failed to create directory '{directory_path}'. {e.strerror}")
        return False

def read_json_file(file_path) -> dict:
    """
    Read a JSON file and parse its contents.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: A dictionary containing the parsed JSON data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Unable to parse JSON file '{file_path}'. {e}")
        return None

def list_folders(path) -> list:
    """
    List all folder names under the given path.
    
    Args:
        path (str): The path to the directory.
    """
    try:
        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        return folders
    except FileNotFoundError as e:
        os.mkdir(path)
        return []
    except OSError as e:
        print(f"Error: {e.strerror}")

def find_files(directory, pattern) -> list:
    """
    Find files within a directory that match a specific pattern.

    Args:
    - directory: The directory to search within.
    - pattern: The pattern to match files against.

    Returns:
    - A list of relative paths of matching files.
    """
    files = []
    for file in glob.glob(os.path.join(directory, pattern)):
        if os.path.isfile(file):
            files.append(os.path.relpath(file, directory))
    return files

def load_env_vars_from_bash(bash_file_path):
    """
    Load environment variables from a bash file and make them available within the Python process scope.
    
    Args:
        bash_file_path (str): Path to the bash file.
    """
    with open(bash_file_path, 'r') as bash_file:
        bash_content = bash_file.read()
        
    # Regex pattern to match lines containing environment variable assignments
    pattern = r'export\s+([^\s=]+)\s*=\s*([^\n]+)\n'
    
    # Extract environment variable assignments
    matches = re.findall(pattern, bash_content)
    
    # Set environment variables in Python process scope
    for match in matches:
        var_name, var_value = match
        os.environ[var_name] = var_value.strip("'\"")

