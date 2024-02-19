import os 
import os
import platform

# Create Folder
def create_folder(folder_name):
    # Get the absolute path of the folder
    path = os.path.abspath(folder_name)

    # Check the operating system
    if platform.system() == 'Windows':
        path = os.path.join('C:', os.sep, path)
    else:
        path = os.path.join('/', path)

    # Check if the folder already exists
    if os.path.exists(path):
        print(f'The folder "{folder_name}" already exists at {path}')
        print('Please choose another name.')
    else:
        # Create the folder
        os.makedirs(path, exist_ok=True)  # Use exist_ok=True for recursive creation
        print(f'Folder "{folder_name}" has been created successfully at {path}')

# Delete Folder
def delete_folder(folder_name):
    path = os.path.abspath(folder_name)

    if platform.system() == 'Windows':
        path = os.path.join('C:', os.sep, path)
    else:
        path = os.path.join('/', path)

    if os.path.exists(path):
        os.rmdir(path)
        print(f'Folder "{folder_name}" deleted successfully.')
    else:
        print(f'The folder named "{folder_name}" does not exist.')


# Search Applications/Files/Folders
def search_manager(application_name, directory):
    found_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if application_name.lower() in file.lower():
                found_paths.append(os.path.join(root, file))
    return found_paths

if __name__ == "__main__":
    application_name = "chrome.exe"
    search_directory = "C:\\Program Files"  

    found_paths = find_application(application_name, search_directory)
    if found_paths:
        print(f"Found {len(found_paths)} instances of {application_name}:")
        for path in found_paths:
            print(path)
    else:
        print(f"No instances of {application_name} found in {search_directory}")

