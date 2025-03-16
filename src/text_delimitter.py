
"""
This module provides functionality to parse and convert markdown-like text into a list of TextNode objects. 
It supports parsing for bold, italic, and code delimiters, as well as markdown-style images and links.
Classes:
    Symbol(Enum): An enumeration for markdown symbols such as CODE, BOLD, and ITALIC.
Functions:
    split_nodes_delimiter(old_nodes, delimiter, text_type):
        Splits TextNodes based on a markdown delimiter.
    extract_markdown_images(text):
        Finds all markdown-style images in text.
    extract_markdown_links(text):
        Finds all markdown-style links in text.
    split_nodes_images(old_nodes):
        Splits text nodes containing markdown-style images.
    split_nodes_links(old_nodes):
        Splits text nodes containing markdown-style links.
    text_to_textnodes(text):
        Converts a markdown-like string into a list of TextNode objects.
"""
from textnode import TextNode, TextType
from enum import Enum
import re

class Symbol(Enum):
    CODE = "`"
    BOLD = "**"
    ITALIC = "_"
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits TextNodes based on a markdown delimiter."""
    final_nodes_output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes_output.append(node)
            continue

        updated_words = node.text.split(delimiter)
        if len(updated_words) % 2 == 0:
            raise ValueError(
                f"Invalid markdown, {text_type.value} section not closed")

        for i, word in enumerate(updated_words):
            if word:
                new_type = text_type if i % 2 == 1 else TextType.TEXT
                final_nodes_output.append(TextNode(word, new_type))

    return final_nodes_output


def extract_markdown_images(text):
    """Finds all markdown-style images in text."""
    pattern = r"!\[([^\[\]]+)\]\(([^()\s]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """Finds all markdown-style links in text."""
    pattern = r"(?<!!)\[([^\[\]]+)\]\(([^()\s]+)\)"
    return re.findall(pattern, text)


def split_nodes_images(old_nodes):
    """Splits text nodes containing markdown-style images."""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if not images and ("![" in original_text or "]" in original_text):
            raise ValueError("Invalid markdown syntax for image")

        for image_name, image_url in images:
            markdown_syntax = f"[{image_name}]({image_url})"
            if markdown_syntax not in original_text:
                raise ValueError("Invalid markdown syntax for images")
            updated_texts = original_text.split(
                f"![{image_name}]({image_url})", 1)
            if len(updated_texts) != 2:
                raise ValueError("Invalid markdown for images")
            if updated_texts[0]:
                new_nodes.append(TextNode(updated_texts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_name, TextType.IMAGE, image_url))
            original_text = updated_texts[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes):
    """Splits text nodes containing markdown-style links."""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if not links and ("[" in original_text or "]" in original_text):
            raise ValueError("Invalid markdown syntax for link")

        for link_name, link_url in links:
            markdown_syntax = f"[{link_name}]({link_url})"
            if markdown_syntax not in original_text:
                raise ValueError("Invalid markdown syntax for links")
            
            updated_texts = original_text.split(markdown_syntax, 1)
            if len(updated_texts) != 2:
                raise ValueError("Invalid markdown for links")
            if updated_texts[0]:
                new_nodes.append(TextNode(updated_texts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_name, TextType.LINK, link_url))
            original_text = updated_texts[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """Converts a markdown-like string into a list of TextNode objects."""
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = {'**': TextType.BOLD,
                  '_': TextType.ITALIC, '`': TextType.CODE}

    for delimiter, text_type in delimiters.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    return nodes


# text = "This is **bold** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
# result = text_to_textnodes(text)
# for node in result:
#     print(node)

    