import os
import re

from markdown_blocks import markdown_to_html_node

def generate_pages(content_path: str, template_path: str, destination_path: str):

    if not os.path.exists(content_path):
        os.mkdir(content_path)

    files = os.listdir(content_path)
    for file in files:
        source_file_path = os.path.join(content_path, file)
        if file.endswith(".md") and os.path.isfile(source_file_path):
            destination_file_path = os.path.join(destination_path, file[:-2] + "html")
            generate_page(source_file_path, template_path, destination_file_path)
        if os.path.isdir(source_file_path):
            destination_file_path = os.path.join(destination_path, file)
            generate_pages(source_file_path, template_path, destination_file_path)
    return

def extract_title(markdown: str):
    headings = [ block.strip() for block in re.split("\n{2,}", markdown) if block.strip().startswith("# ") ]
    
    if len(headings) != 1:
        raise ValueError("No title found")
    
    return headings[0].lstrip("# ")

def generate_page(content_path, template_path, destination_path):
    f = open(content_path,"r")
    markdown = f.read()
    f.close()
    f = open(template_path,"r")
    template = f.read()
    f.close()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    html_out = template.replace("{{ Content }}", content).replace("{{ Title }}", title)

    destination_directory = os.path.dirname(destination_path)

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    f = open(destination_path,"x")
    f.write(html_out)
    f.close
    return
