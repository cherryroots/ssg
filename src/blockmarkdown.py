from typing import List
from htmlnode import ParentNode, LeafNode
from inlinemarkdown import text_to_textnodes
from textnode import text_node_to_html_node
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_html_node(markdown:str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    root = ParentNode("div", [])
    for block in blocks:
        new_node = block_to_html_node(block)
        root.children.append(new_node)
    return root

def block_to_html_node(block:str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        tag = "p"
        block = " ".join(block.split("\n"))
        textNodes = text_to_textnodes(block)
        children = [text_node_to_html_node(textNode) for textNode in textNodes]
        return ParentNode(tag, children)
    
    if block_type == block_type_heading:
        header_level = block.count("#")
        tag = f"h{header_level}"
        block = "\n".join(map(lambda w: w.lstrip("# "), block.split("\n")))
        textNodes = text_to_textnodes(block)
        children = [text_node_to_html_node(textNode) for textNode in textNodes]
        return ParentNode(tag, children)
    
    if block_type == block_type_code:
        tag = "pre"
        children = [LeafNode("code", block.strip("```"))]
        return ParentNode(tag, children)
    
    if block_type == block_type_quote:
        tag = "blockquote"
        block = " ".join(map(lambda w: w.lstrip("> "), block.split("\n")))
        textNodes = text_to_textnodes(block)
        children = [text_node_to_html_node(textNode) for textNode in textNodes]
        return ParentNode(tag, children)
    
    if block_type == block_type_ulist:
        tag = "ul"
        block = "\n".join(map(lambda w: w.lstrip("- "), block.split("\n")))
        textNodeLines = [text_to_textnodes(line) for line in block.splitlines()]
        leafNodes = [[text_node_to_html_node(textNode) for textNode in line] for line in textNodeLines]
        children = [ParentNode("li", leafnodes) for leafnodes in leafNodes]
        return ParentNode(tag, children)
    
    if block_type == block_type_olist:
        tag = "ol"
        block = "\n".join(map(lambda w: w.split(". ", 1)[1], block.split("\n")))
        textNodeLines = [text_to_textnodes(line) for line in block.splitlines()]
        leafNodes = [[text_node_to_html_node(textNode) for textNode in line] for line in textNodeLines]
        children = [ParentNode("li", leafnodes) for leafnodes in leafNodes]
        return ParentNode(tag, children)

def block_to_block_type(block:str) -> str:
    heading_regex = re.compile(r"^(#{1,6}) (.*)", re.MULTILINE)
    codeblock_regex = re.compile(r"^(`{3})\n*?(.*)\n*?(`{3})$", re.MULTILINE)
    quote_regex = re.compile(r"^>", re.MULTILINE)
    ul_regex = re.compile(r"^[-*] ", re.MULTILINE)
    ol_regex = re.compile(r"^\d[.] ", re.MULTILINE)

    headings = re.findall(heading_regex, block)
    codeblock = re.findall(codeblock_regex, block)
    quotes = re.findall(quote_regex, block)
    uls = re.findall(ul_regex, block)
    ols = re.findall(ol_regex, block)

    lines = block.splitlines()
    if len(headings) == len(lines):
        return block_type_heading
    if len(codeblock) > 0:
        return block_type_code
    if len(quotes) == len(lines):
        return block_type_quote
    if len(uls) == len(lines):
        return block_type_ulist
    if len(ols) == len(lines) and is_valid_ol(lines):
        return block_type_olist
    return block_type_paragraph

def is_valid_ol(lines: List[str]):
    return all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines))

def markdown_to_blocks(markdown:str) -> List[str]:
    return [block.strip("\n") for block in markdown.split("\n\n") if block is not ""]