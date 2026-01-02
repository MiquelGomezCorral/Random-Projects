"""Main file for scripts with arguments and call other functions."""

import argparse
import shutil
import os
import platform
from tqdm import tqdm
from datetime import datetime
from maikol_utils.file_utils import list_dir_files
from maikol_utils.print_utils import print_separator

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


def creation_date(path_to_file):
    """
    Get the Unix timestamp that a file was last modified.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    
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