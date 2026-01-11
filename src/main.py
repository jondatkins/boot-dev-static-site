import os
import shutil
import sys

from pathlib import Path
from markdown_processing import markdown_to_html_node

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT_NAME = "static_site"


def main():
    # Checking if an argument is provided before accessing it
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]  # First argument

    dest_dir_name = "docs"
    dest_dir_path = f"{BASE_DIR}/{dest_dir_name}"
    source_static_dir = "static"
    source_static_dir_path = f"{BASE_DIR}/{source_static_dir}"
    source_content_dir = "content"
    source_content_dir_path = f"{BASE_DIR}/{source_content_dir}"

    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    os.mkdir(dest_dir_path)
    copy_files(source_static_dir_path, source_static_dir, dest_dir_name)
    file_paths, dir_paths = get_file_paths(f"{BASE_DIR}/content")
    src_and_dest_file_paths = []
    for file in file_paths:
        dest_file_path = file.replace(f"/{source_content_dir}/", f"/{dest_dir_name}/")
        dest_file_path = dest_file_path.replace(".md", ".html")
        src_and_dest_file_paths.append((file, dest_file_path))
    # Create correct directories for html files
    for dir in dir_paths:
        dest_dir_path = dir.replace(f"/{source_content_dir}/", f"/{dest_dir_name}/")
        os.mkdir(dest_dir_path)
    # print(src_and_dest_file_paths)
    for files in src_and_dest_file_paths:
        generate_page(files[0], f"{BASE_DIR}/template.html", files[1], basepath)

    # for md_file in file_paths:
    #     generate_page(md_file, f"{BASE_DIR}/template.html", f"{BASE_DIR}/")
    # copy_source_to_public("content", "public")
    # print(f"files: {file_paths}")
    # print(f"dirs: {dir_paths}")
    # markdown_files = [
    #     "",
    #     "blog/glorfindel/",
    #     "blog/tom/",
    #     "blog/majesty/",
    #     "contact/",
    # ]
    # for file_path in markdown_files:
    #     generate_page(
    #         f"{BASE_DIR}/content/{file_path}index.md",
    #         f"{BASE_DIR}/template.html",
    #         f"{BASE_DIR}/public/{file_path}index.html",
    #     )
    #


def extract_title(markdown):
    lines = markdown.split("\n")
    heading_one = []
    for line in lines:
        line = line.strip()
        if line.startswith(("# ")):
            heading_one = line.split("# ", 1)
            if len(heading_one) != 2:
                raise ValueError(f"Heading 1 '# ' not found for markdown: {markdown}")
            return heading_one[1].strip()
    raise ValueError(f"Heading 1 '# ' not found for markdown: {markdown}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pass


def generate_page(from_path, template_path, dest_path, basepath):
    #  Print a message like "Generating page from from_path to dest_path using template_path".
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file at from_path and store the contents in a variable.

    markdown_file = read_file(from_path)

    # Read the template file at template_path and store the contents in a variable.
    template_html = read_file(template_path)

    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    markdown_html = markdown_to_html_node(markdown_file).to_html()
    # markdown_html = f"{markdown_html}"
    # Use the extract_title function to grab the title of the page.
    page_title = extract_title(markdown_file)
    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    template_html = template_html.replace("{{ Title }}", page_title)
    template_html = template_html.replace("{{ Content }}", markdown_html)
    template_html = template_html.replace('href="/', f'href="{basepath}"')
    template_html = template_html.replace('src="/', f'src="{basepath}"')
    # Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    dest_dirs = dest_path.split(PROJECT_ROOT_NAME, 1)
    # Just get the directories inside the project folder
    project_dirs = dest_dirs[1]
    root_dirs = dest_dirs[0] + PROJECT_ROOT_NAME
    project_dirs = project_dirs.split("/")
    project_dirs = project_dirs[1:-1]
    full_dir_path = root_dirs
    # Make sure that directories exist. Could just use makedirs
    for dir in project_dirs:
        if dir == "":
            continue
        full_dir_path = f"{full_dir_path}/{dir}"
        if not os.path.exists(full_dir_path):
            os.mkdir(full_dir_path)

    write_file(template_html, dest_path)


def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        read_data = f.read()
    f.closed
    return read_data


def write_file(file_contents, dest_path):
    # lines = ["First line\n", "Second line\n", "Third line\n"]
    with open(dest_path, "w") as f:
        f.writelines(file_contents)


# Takes the src dir, e.g. 'static' and the dest dir, e.g. 'public'.
# These are assumed to be folders at the top level of the project
def copy_source_to_public(src, dest):
    source_path = f"{BASE_DIR}/{src}"
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_files(source_path, src, dest)


# Copy files from a given directory, e.g. 'static' to another dir, most likely
# 'public'. Copy files uses the recursive function get_file_paths to get a list of file
# paths and directory paths, so that the correct folders can be created before copying the
# files to their right location relative to the 'public' folder. For example, 'static/images/
# tolkien.png' is copied to 'public/images/tolkien.png'
def copy_files(src_dir_path, content_dir_name, dest_dir_name):
    file_paths, dir_paths = get_file_paths(src_dir_path)
    for dir in dir_paths:
        dest_dir_path = dir.replace(f"/{content_dir_name}/", f"/{dest_dir_name}/")
        os.mkdir(dest_dir_path)

    for file in file_paths:
        dest_file_path = file.replace(f"/{content_dir_name}/", f"/{dest_dir_name}/")
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
