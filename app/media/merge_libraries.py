import os

# Merge library type
# Inputs:
# - media_type: string. e.g. 'tv', 'movies'
# - quality_list: array of strings. e.g. ['4k', 'uhd', 'hd', 'sd']
# - source_paths: array of folder base paths
# - merged_path: folder base path for merged media
# Outputs:
# - bool: True if merge was successful, False otherwise

def merge_libraries(media_type: str, source_paths: list[str], quality_list: list[str], merged_path: str) -> bool:
    success = True
    for source_path in source_paths:
        for quality in quality_list:
            media_folder = f"{media_type}-{quality}"
            
            media_path = f"{source_path}/{media_folder}"
            print(f"Media path: {media_path}")
            print(f"Merging {media_type} from {media_path} to {merged_path}")

            # Get all folders in media_path if it exists
            if os.path.exists(media_path):
                folders = os.listdir(media_path)
                print(f"Folders: {folders}")

                # For each folder, call merge_folder
                for folder in folders:
                    merge_folder(folder, merged_path, quality_list)

            # Create target media path
#            target_path = f"{merged_path}/{media_folder}"
 #           print(f"Target path: {target_path}")    

            # If target_path folder does not exist, create it
#            if not os.path.exists(target_path):
#                print(f"Target path {target_path} does not exist, creating it")
#                os.makedirs(target_path)###

                # Make correct user and group ownership
#                os.chown(target_path, 1000, 1000)

            # Call get folder_flags method
 #           folder_flags = get_folder_flags(target_path)
  #          print(f"Folder flags: {folder_flags}")

    return success  

# Get folder flag
# A folder flag is a file starting with '.' with rest of name being the flag name
# Outputs:
# - array of strings representing the flag names
def get_folder_flags(media_path: str) -> list[str]:
    folder_flags = []
    for file in os.listdir(media_path):
        if file.startswith('.'):
            folder_flags.append(file[1:])
    return folder_flags

# Get folder quality flags
# Inputs:
# - folder: string. e.g. 'tv-4k'
# Outputs:
# - the quality type, so the found flag files need to match with quality array
def get_folder_quality_flags(folder: str, quality_list: list[str]) -> str:
    # get folder flags and see if any of them match with quality_list
    folder_flags = get_folder_flags(folder)
    for flag in folder_flags:
        if flag in quality_list:
            return flag
    return None

def merge_folder(folder: str, merged_path: str, quality_list: list[str]) -> bool:
    success = True

    # See if folder exists in merged_path, and create it if it doesn't
    if not os.path.exists(f"{merged_path}/{folder}"):
        print(f"Folder {folder} does not exist in {merged_path}, creating it")
        os.makedirs(f"{merged_path}/{folder}")

    # call get_folder_flags on the folder
    folder_quality_flag = get_folder_quality_flags(f"{merged_path}/{folder}", quality_list)
    print(f"Folder quality flag: {folder_quality_flag}")

    