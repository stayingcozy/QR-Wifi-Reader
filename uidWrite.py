import os

def write_uid(uid):
    # Get the home directory
    home_dir = os.path.expanduser("~")

    # Specify the file path
    file_path = os.path.join(home_dir, "uid.txt")

    # Write the string to the file
    with open(file_path, 'w') as file:
        file.write(uid)
