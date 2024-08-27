import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,


)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # create a list of TextNodes
    textNodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            textNodes.append(old_node)
            continue
        new_nodes = []
        node_list = old_node.text.split(delimiter)
        if len(node_list) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(node_list)):
            if node_list[i] == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(node_list[i], text_type))
            else:
                new_nodes.append(TextNode(node_list[i], text_type_text))
        textNodes.extend(new_nodes)
    return textNodes


def extract_markdown_images(text):
    imgRegex = r"!\[(.*?)\]\((.*?)\)"
    images = re.findall(imgRegex, text)
    return images


def extract_markdown_links(text):
    linkRegex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    links = re.findall(linkRegex, text)
    return links


def split_nodes_image(old_nodes):
    textNodes = []
    for old_node in old_nodes:
        text = old_node.text
        if old_node.text_type != text_type_text:
            textNodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            textNodes.append(old_node)
            continue
        for image in images:
            if text == "":
                continue
            image_alt = image[0]
            image_link = image[1]
            print(image_alt, image_link)
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                textNodes.append(TextNode(sections[0], text_type_text))
            textNodes.append(TextNode(image_alt, text_type_image, image_link))
            text = sections[1]
        if text != "":
            textNodes.append(TextNode(text, text_type_text))
    return textNodes


def split_nodes_link(old_nodes):
    textNodes = []
    for old_node in old_nodes:
        text = old_node.text
        if old_node.text_type != text_type_text:
            textNodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            textNodes.append(old_node)
            continue
        for link in links:
            if text == "":
                continue
            link_alt = link[0]
            link_link = link[1]
            sections = text.split(f"[{link_alt}]({link_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                textNodes.append(TextNode(sections[0], text_type_text))
            textNodes.append(TextNode(link_alt, text_type_link, link_link))
            text = sections[1]
        if text != "":
            textNodes.append(TextNode(text, text_type_text))
    return textNodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def main():

    node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        text_type_text,
    )

    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))


main()
