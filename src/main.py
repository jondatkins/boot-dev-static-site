from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import os
import shutil

from pathlib import Path


SRC_DIR = "static"
DEST_DIR = "public"


def main():
    copy_source_to_public()


def extract_title(markdown):
    pass


def copy_source_to_public():
    base_dir = Path(__file__).resolve().parent.parent
    source = base_dir / SRC_DIR
    dest = base_dir / DEST_DIR
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_files(source)


def copy_files(src):
    file_paths, dir_paths = get_file_paths(src)
    for dir in dir_paths:
        dest_dir_path = dir.replace(f"/{SRC_DIR}/", f"/{DEST_DIR}/")
        os.mkdir(dest_dir_path)

    for file in file_paths:
        dest_file_path = file.replace(f"/{SRC_DIR}/", f"/{DEST_DIR}/")
        shutil.copy(file, dest_file_path)


# Loop over the files and directories in the src dir
#     if we're looking at a file, add it to 'file_paths'
#     Otherwise, add the dir path to 'dir_paths', and then
#     recursively get the file and dir paths, which we add to the
#     end of the file and dir path lists
def get_file_paths(src):
    list_dirs = os.listdir(src)
    file_paths = []
    dir_paths = []
    for file in list_dirs:
        file_path = os.path.join(src, file)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
        else:
            dir_paths.append(file_path)
            fl_pth, dr_pth = get_file_paths(file_path)
            file_paths.extend(fl_pth)
            dir_paths.extend(dr_pth)

    return file_paths, dir_paths


if __name__ == "__main__":
    main()
