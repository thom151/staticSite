from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_olist,
    block_type_ulist,
    markdown_to_html_node,
)
import os
from pathlib import Path


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generate page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    from_contents = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template_contents = template_file.read()
    template_file.close()

    html_nodes = markdown_to_html_node(from_contents).to_html()
    title = extract_title(from_contents)

    replaced_title = template_contents.replace("{{ Title }}", title)
    replaced_contents = replaced_title.replace("{{ Content }}", html_nodes)
    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(replaced_contents)
    dest_file.close()


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir = os.listdir(dir_path_content)
    for file in content_dir:
        from_path = os.path.join(dir_path_content, file)
        dest_path = Path(os.path.join(dest_dir_path, file))
        if os.path.isfile(from_path):
            generate_page(from_path, template_path,
                          dest_path.with_suffix('.html'))
        else:
            generate_page_recursive(from_path, template_path, dest_path)
