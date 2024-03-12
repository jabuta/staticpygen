from generatepage import generate_page, generate_pages
from renamefiles import repl_directory
import os
import shutil

static_path = "./static"
content_path = "./content"
template = "./template.html"
public_path = "./public"


def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    repl_directory(static_path, public_path)
    generate_pages(content_path, template, public_path)

main()