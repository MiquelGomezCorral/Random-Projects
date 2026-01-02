"""Main file for scripts with arguments and call other functions."""

import argparse
import shutil
import os
import platform
from tqdm import tqdm
from datetime import datetime
from maikol_utils.file_utils import list_dir_files
from maikol_utils.print_utils import print_separator

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

def main(args: argparse.Namespace):
    """Main function to move photos based on date.

    Args:
        args (argparse.Namespace): Command line arguments.
    """
    print_separator("MOVE PHOTOS BASED ON DATE", sep_type="START")
    input_folder = args.input_folder
    output_folder = args.output_folder
    recursive = args.recursive
    limit_date = datetime.strptime(args.limit_date, '%Y-%m-%d').date()
    filter_negative = args.filter_negative
    filter_positive = args.filter_positive

    print(f" - Input folder:  {input_folder}")
    print(f" - Output folder: {output_folder}")
    print(f" - Recursive:     {recursive}")
    print(f" - Limit date:    {limit_date}")

    print_separator("PROCESSING FILES", sep_type="LONG")

    files, _ = list_dir_files(input_folder, recursive=recursive, absolute_path=True)

    for f in tqdm(files):
        print(f"Processing file: {f}")
        time = creation_date(f)
        file_name = os.path.basename(f)
        output_path = os.path.join(output_folder, file_name)

        if time is None:
            print(f"Could not determine creation date for file: {f}")
            continue

        if filter_negative:
            if any(fn in file_name for fn in filter_negative):
                # print(f"Skipping file due to negative filter: {f}")
                continue
        if filter_positive:
            if not any(fp in file_name for fp in filter_positive):
                # print(f"Skipping file due to positive filter: {f}")
                continue
        
        if datetime.fromtimestamp(time).date() > limit_date:
            shutil.copy2(f, output_path)




def get_exif_date(path_to_file):
    """Extract creation date from EXIF data if available."""
    if not PILLOW_AVAILABLE:
        return None
    
    try:
        image = Image.open(path_to_file)
        exif_data = image._getexif()
        if exif_data is None:
            return None
        
        # Look for DateTimeOriginal (when photo was taken)
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == 'DateTimeOriginal':
                # Parse EXIF date format: "YYYY:MM:DD HH:MM:SS"
                dt = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                return dt.timestamp()
        return None
    except Exception:
        return None


def creation_date(path_to_file):
    """
    Try to get the Unix timestamp that a file was created.
    For photos, tries EXIF data first, then falls back to file system metadata.
    """
    # Try EXIF data for image files
    exif_time = get_exif_date(path_to_file)
    if exif_time is not None:
        return exif_time
    
    # Try birthtime on systems that support it (macOS, Windows)
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    
    stat = os.stat(path_to_file)
    try:
        # macOS/BSD have st_birthtime
        return stat.st_birthtime
    except AttributeError:
        # Linux doesn't reliably support birth time
        # Fall back to modification time
        return os.path.getmtime(path_to_file)


# ======================================================================================
#                                       ARGUMENTS
# ======================================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="app", description="Main Application CLI")

    parser.add_argument(
        "-i", "--input_folder", type=str, required=True, help="Path to input folder with all folders and photos"
    )
    parser.add_argument(
        "-o", "--output_folder", type=str, required=True, help="Path to output folder where photos will be moved"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_false", default=True, help="Disable recursive search in input folder"
    )
    parser.add_argument(
        "-d", "--limit_date", type=str, required=True, help="Limit date for moving photos in format YYYY-MM-DD"
    )
    parser.add_argument(
        "-fn", "--filter-negative", type=str, nargs='*', default=None, help="Filter strings that the files must not contain (example: .mp4 .mov for videos)"
    )
    parser.add_argument(
        "-fp", "--filter-positive", type=str, nargs='*', default=None, help="Filter strings that the files must contain (example: IMG_ DSC_)"
    )
    
    

    args = parser.parse_args()
    main(args)