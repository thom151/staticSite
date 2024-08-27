
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    list = markdown.split("\n\n")
    for item in list:
        if item == "":
            continue
        blocks.append(item.strip())
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if (block.startswith("# ")
            or block.startswith("## ")
            or block.startswith("### ")
            or block.startswith("#### ")
            or block.startswith("##### ")
            or block.startswith("###### ")
        ):
        return block_type_heading

    elif block.startswith("> "):
        return block_type_quote

    elif "```" == block[:3] and "```" == block[-3:]:
        return block_type_code

    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist

    if block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return block_type_paragraph
        return block_type_olist
    return block_type_paragraph


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return to_paragraph_html(block)
    if block_type == block_type_heading:
        return to_headings_html(block)
    if block_type == block_type_code:
        return to_code_html(block)
    if block_type == block_type_olist:
        return to_ol_html(block)
    if block_type == block_type_ulist:
        return to_ul_html(block)
    if block_type == block_type_quote:
        return to_quote_html(block)
    raise ValueError("Invalid block type")


def to_paragraph_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def to_headings_html(block):
    level = 0
    for char in block:
        if char != "#":
            break
        level += 1
    hastags, text = block.split("# ")
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def to_code_html(block):
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def to_quote_html(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote")
        cleaned_lines.append(line.lstrip(">").strip())
    text = " ".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def to_ul_html(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[2:]
        li_children = text_to_children(text)
        li_nodes.append(ParentNode("li", li_children))
    return ParentNode("ul", li_nodes)


def to_ol_html(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[3:]
        li_children = text_to_children(text)
        li_nodes.append(ParentNode("li", li_children))
    return ParentNode("ol", li_nodes)


def text_to_children(text):
    htmlNodes = []
    textNodes = text_to_textnodes(text)
    for node in textNodes:
        htmlNodes.append(text_node_to_html_node(node))
    return htmlNodes


def main():
    text = """# This is a heading


    This is a paragraph of text. It has some ** bold ** and *italic * words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item"
    """

    markdown_to_html_node(text)


if __name__ == "__main__":
    main()
