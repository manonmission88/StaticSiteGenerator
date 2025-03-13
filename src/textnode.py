
from leafnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text 
        self.text_type = text_type 
        self.url = url 
        
    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url 
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

'''
convert text node to leaf nodes 

'''
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", value=text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("a", value=text_node.anchor_text, props={"href": text_node.value})
    elif text_node.text_type == TextType.LINK:
        return LeafNode("img", value="", props={"src": text_node.value, "alt": text_node.alt_text})
    raise ValueError("Need valid text")

    