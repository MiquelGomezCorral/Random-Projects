import os
import argparse
import rawpy
from PIL import Image
from tqdm import tqdm

from maikol_utils.print_utils import print_separator
from maikol_utils.file_utils import list_dir_files, make_dirs

def main(args):
    print_separator("PROCESSING IMAGES TO REDUCE QUALITY AND SIZE", sep_type="START")
    make_dirs(args.output_folder_path)
    list_files, n = list_dir_files(args.input_folder_path)
    print(f"- Total files to process: {n}")
    
    for file_path in tqdm(list_files):
        process_image(file_path, args.output_folder_path)

    print_separator("DONE!", sep_type="START")


def process_image(file_path, output_folder_path):
    file_name = file_path.split('/')[-1]
    output_file_path = os.path.join(output_folder_path, file_name.split('.')[0] + '.png')

    # Read RAW image and make it RGB: they are in raw format so the image is not 'standard'
    with rawpy.imread(file_path) as raw:
        rgb = raw.postprocess()
    img = Image.fromarray(rgb)

    # resize (example: max width 2000px, keep ratio)
    img.thumbnail((args.size, args.size), Image.LANCZOS)
    img.save(output_file_path, optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="reduce_quality", description="Main Application CLI. Example of usage: python ./src/images/reduce_quality.py -i /mnt/c/Users/mique/Desktop/SyncMaikol/.Importantes/.Fotos/Fotos/Poland/all -o /mnt/c/Users/mique/Desktop/SyncMaikol/.Importantes/.Fotos/Fotos/Poland/all_reduced/ ")

    parser.add_argument(
        "-i", "--input_folder_path", type=str, required=True, help="Path to the input folder"
    )
    parser.add_argument(
        "-o", "--output_folder_path", type=str, required=True, help="Path to the output folder"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=2000, help="Max size for the longest edge of the image"
    )

    args = parser.parse_args()
    main(args)