import os
import shutil
from datetime import datetime
from PIL import Image
import sys

def organize_files_by_year(src_folder):
    """
    Organizes images and videos in the specified folder into subfolders by year.

    Parameters:
    src_folder (str): The path to the source folder containing the images and videos.

    The function will check each file's creation date and move it to a folder
    named 'picture {year}' or 'video {year}' within the source folder. If a folder for the year
    doesn't exist, it will be created. The function prints a summary of the
    process, including the number of files moved and not moved.
    """

    # Check if the source folder is valid
    if not os.path.isdir(src_folder):
        print("Invalid folder path.")
        return

    # Check if the source folder is empty
    if not os.listdir(src_folder):
        print("The folder is empty.")
        return

    moved_count = 0  # Counter for moved files
    not_moved_count = 0  # Counter for files that couldn't be moved

    # Iterate through each file in the source folder
    for filename in os.listdir(src_folder):
        # Check if the file is an image or video
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4')):
            file_path = os.path.join(src_folder, filename)
            try:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    # Extract the creation date from the image metadata
                    img = Image.open(file_path)
                    img_exif = img._getexif()
                    if img_exif is not None:
                        creation_date = img_exif.get(36867)
                        if creation_date is not None:
                            year = creation_date[:4]
                        else:
                            year = datetime.fromtimestamp(os.path.getmtime(file_path)).year
                    else:
                        year = datetime.fromtimestamp(os.path.getmtime(file_path)).year

                    # Create the folder name based on the year
                    folder_name = f'picture {year}'
                elif filename.lower().endswith('.mp4'):
                    # Extract the creation date from the file metadata
                    year = datetime.fromtimestamp(os.path.getmtime(file_path)).year

                    # Create the folder name based on the year
                    folder_name = f'video {year}'

                year_folder = os.path.join(src_folder, folder_name)
                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)

                # Move the file to the appropriate year folder
                shutil.move(file_path, os.path.join(year_folder, filename))
                moved_count += 1  # Increment the moved count
            except Exception as e:
                not_moved_count += 1  # Increment the not moved count
                print(f"Error processing file {filename}: {e}")

    # Print the summary of the process
    print(f"Process completed. {moved_count} files moved, {not_moved_count} files not moved.")

if __name__ == "__main__":
    # Check if the script is run with the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <source_folder_path>")
    else:
        src_folder = sys.argv[1]
        organize_files_by_year(src_folder)
