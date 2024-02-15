import os 

# Create Folder
def create_folder(folder_name):
    path = os.path.abspath(folder_name)

    if os.path.exists(path):
        print(f'The folder "{folder_name}" already exists at {path}')
        print( 'Please choose another name.' )
    else:
        os.mkdir(path)
        print(
             f'Folder "{folder_name}" has been created successfully at {path}')

# Delete Folder
def delete_folder(folder_name):
    path = os.path.abspath(folder_name)

    if os.path.exists(path):
        os.rmdir(path)
        print(f'Folder "{folder_name}" deleted successfully.')
    else:
        print(f'The folder named "{folder_name}" does not exist.')
