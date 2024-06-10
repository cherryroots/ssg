from htmlnode import LeafNode
from textnode import *
from typing import List
import re

def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str, text_type:str) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        delimiter_count = node.text.count(delimiter)

        if delimiter_count == 0:
            new_nodes.append(node)
            continue

        if delimiter_count % 2 != 0:
            raise Exception("Invalid markdown: only one of two delimiters found")
        
        new_text = node.text
        for i in range(1, delimiter_count+1):
            text_parts = new_text.split(delimiter, 1)
            new_text = text_parts[1]
            if i % 2 == 0:
                new_nodes.append(TextNode(text_parts[0], text_type, node.url))
            else:
                new_nodes.append(TextNode(text_parts[0], node.text_type))
            if i == delimiter_count and len(new_text) != 0:
                new_nodes.append(TextNode(text_parts[1], node.text_type))  

    return new_nodes

def split_nodes_image(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        new_text = node.text
        for i, image in enumerate(images):
            text_parts = new_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(text_parts) != 2:
                raise Exception("Invalid markdown: image was not properly closed")
            new_text = text_parts[-1]
            if len(text_parts[0]) > 0:
                new_nodes.append(TextNode(text_parts[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            if i == len(images) - 1 and len(new_text) != 0:
                new_nodes.append(TextNode(text_parts[1], text_type_text)) 

    return new_nodes

def split_nodes_link(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        new_text = node.text
        for i, link in enumerate(links):
            text_parts = new_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(text_parts) != 2:
                raise Exception("Invalid markdown: link was not properly closed")
            new_text = text_parts[-1]
            if len(text_parts[0]) > 0:
                new_nodes.append(TextNode(text_parts[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            if i == len(links) - 1 and len(new_text) != 0:
                new_nodes.append(TextNode(text_parts[1], text_type_text)) 


    return new_nodes

def extract_markdown_images(markdown:str) -> List[str]:
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, markdown)
    return matches

def extract_markdown_links(markdown:str) -> List[str]:
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, markdown)

    return matches

def text_to_textnodes(text:str) -> List[TextNode]:
    node = [TextNode(text, text_type_text)]
    node = split_nodes_delimiter(node, "**", text_type_bold)
    node = split_nodes_delimiter(node, "*", text_type_italic)
    node = split_nodes_delimiter(node, "`", text_type_code)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node