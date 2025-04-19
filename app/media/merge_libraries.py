import os

# Merge library type
# Inputs:
# - media_type: string. e.g. 'tv', 'movies'
# - quality_list: array of strings. e.g. ['4k', 'uhd', 'hd', 'sd']
# - source_paths: array of folder base paths
# - merged_path: folder base path for merged media
# Outputs:
# - bool: True if merge was successful, False otherwise

def merge_libraries(media_type: str, source_paths: list[str], quality_list: list[str], merged_path: str, user_id: int, group_id: int) -> bool:
    success = True
    for source_path in source_paths:
        for quality in quality_list:
            media_folder = f"{media_type}-{quality}"
            
            media_path = f"{source_path}/{media_folder}"
            #print(f"Media path: {media_path}")
            #print(f"Merging {media_type} from {media_path} to {merged_path}")

            # Get all folders in media_path if it exists
            if os.path.exists(media_path):
                folders = os.listdir(media_path)
                #print(f"Folders: {folders}")

                # For each folder, call merge_folder
                for folder in folders:
                    merge_folder(media_path, folder, merged_path, quality, quality_list, user_id, group_id)

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

def merge_folder(media_path: str, folder: str, merged_path: str, quality: str, quality_list: list[str], user_id: int, group_id: int) -> bool:
    success = True

    # See if folder exists in merged_path, and create it if it doesn't
    source_path = f"{media_path}/{folder}"
    target_path = f"{merged_path}/{folder}"
    if not os.path.exists(target_path):
        #print(f"Folder {folder} does not exist in {merged_path}, creating it")
        try:
            # Create directory with proper permissions
            os.makedirs(target_path, mode=0o755)
            # Set ownership
            os.chown(target_path, user_id, group_id)
        except PermissionError as e:
            #print(f"Error creating directory {target_path}: {str(e)}")
            return False

    # call get_folder_flags on the folder
    folder_quality_flag = get_folder_quality_flags(target_path, quality_list)
    #print(f"Folder quality flag: {folder_quality_flag}")
    
    # Determine if folder_quality_flag is better than quality
    if folder_quality_flag is not None and quality_list.index(folder_quality_flag) < quality_list.index(quality):
        #print(f"Folder quality flag {folder_quality_flag} is better than {quality}, skipping")
        return True

    # Merge folder
    # Create a flag file with current quality
    flag_file = f"{target_path}/.{quality}"
    with open(flag_file, 'w') as f:
        f.write(f"{quality}")
        #print(f"Created flag file {flag_file}")

    # Get all files in folder
    #print(f"Folder path: {source_path}")

    # Recursively hard link all files in source_path to target_path keeping the same relative path
    for root, dirs, files in os.walk(source_path):
        for file in files:
            rel_path = os.path.relpath(root, source_path)
            src = os.path.join(root, file)
            dst_dir = os.path.join(target_path, rel_path)
            dst = os.path.join(dst_dir, file)

            os.makedirs(dst_dir, mode=0o755, exist_ok=True)
            os.chown(dst_dir, user_id, group_id)

            try:
                print(f"Linking {src} to {dst}")
                os.link(src, dst)
            except FileExistsError:
                print(f"Skipping existing file: {dst}")
                pass
            except OSError as e:
                print(f"Failed to link {src} to {dst}: {e}")
                success = False

    return success
