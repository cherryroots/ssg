from textnode import *
from htmlnode import *
from inlinemarkdown import *
from blockmarkdown import *

import os
import shutil

def main():
    generate_page("./content", "./template.html", "./public")
   

def extract_title(markdown:str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No header found in markdown")

def file_content(path:str) -> str:
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    raise Exception("File does not exist")

def write_file(path:str, content:str):
    with open(path, "w") as f:
        f.write(content)
        f.close()

def fill_template(markdown:str, template:str) -> str:
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    return template.replace("{{ Title }}", title).replace("{{ Content }}", html)

def generate_page(src:str, tmpl:str, dst:str):
    if os.path.exists(src) == False:
        raise Exception(f"{src} does not exist")
    if os.path.exists(dst):
        print(f"DELETED: {dst}")
        shutil.rmtree(dst)
    print(f"CREATED: {dst}")
    os.mkdir(dst)

    for file in os.listdir(src):
        srcpath = os.path.join(src, file)
        dstpath = os.path.join(dst, file)
        print(f"GENERATING: {srcpath} -> {dstpath} with {tmpl}")
        if os.path.isfile(srcpath) and srcpath.endswith(".md"):
            markdown = file_content(srcpath)
            template = file_content(tmpl)
            html = fill_template(markdown, template)
            write_file(dstpath.replace(".md", ".html"), html)
        elif os.path.isfile(srcpath):
            shutil.copy(srcpath, dstpath)
        else:
            generate_page(srcpath, tmpl, dstpath)


main()