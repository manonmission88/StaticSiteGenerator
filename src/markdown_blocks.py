"""
It takes a raw Markdown string (representing a full document) 
as input and returns a list of "block" strings.

"""
from enum import Enum 
from htmlnode import HTMLNode
from parent_node import ParentNode
from textnode import TextNode,text_node_to_html_node,TextType
from text_delimitter import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ORDERED_LIST = 'ordered_list'
    UNORDERED_LIST = 'unordered_list'
    
    
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_markdown = []
    for block in blocks:
        if len(block) == 0:
            continue
        final_markdown.append(block.strip())
    return final_markdown

def block_to_block_type(block):
    print(block)
    if block.startswith('#'):
        return BlockType.HEADING
    if block.startswith('>'):
        return BlockType.QUOTE
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    if block.startswith('-'):
        return BlockType.UNORDERED_LIST
    ordered_markers = ('1', 'A', 'a', 'I', 'i')
    if block.startswith(ordered_markers):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
        
    
    
    
    
    
text = """# This is a heading

This is a paragraph of text. 
It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
# markdown_blocks = markdown_to_html_node(text)
# print(markdown_blocks)
# for block in markdown_blocks:
#     print(block,block_to_block_type(block))
