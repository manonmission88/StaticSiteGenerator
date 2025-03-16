from textnode import TextNode, TextType
from enum import Enum
import re
class Symbol(Enum):
    CODE = "`"
    BOLD = "**"
    ITALIC = "_"
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes_output = []
    for node in old_nodes:
        if node.text_type.value != 'text':
            final_nodes_output.append(node)
            continue 
        updated_words = node.text.split(delimiter)
        # print(updated_words)
        if len(updated_words) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for word in updated_words:
            if len(word) >=1:
                if ' '== word[0] or ' '==word[-1]:
                    new_object = TextNode(word,node.text_type)
                    final_nodes_output.append(new_object)
                else:
                    obj = TextNode(word,text_type)
                    final_nodes_output.append(obj)
    return final_nodes_output

def extract_markdown_images(text):
      '''
      takes raw markdown text and returns a list of tuples. 
      Each tuple should contain the alt text and the URL of any markdown images.
    
      '''
      pattern = r'!\[([^\]]*?)\]\((.*?)\)'
      matches = re.findall(pattern, text)
      return matches


def extract_markdown_links(text):
    '''
      takes raw markdown text and returns a list of tuples. 
      Each tuple should contain the alt text and the URL of any markdown links.
    
      '''
    pattern = r'\[([^\]]*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image_name,image_url in images:
            updated_texts = original_text.split(f"![{image_name}]({image_url})", 1)
            if len(updated_texts) != 2:
                raise ValueError("invalid markdown")
            if updated_texts[0] != "":
                new_nodes.append(TextNode(updated_texts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image_name,
                    TextType.IMAGE,
                    image_url,
                )
            )
            original_text = updated_texts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
            

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image_name, image_url in images:
            updated_texts = original_text.split(
                f"[{image_name}]({image_url})", 1)
            if len(updated_texts) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if updated_texts[0] != "":
                new_nodes.append(TextNode(updated_texts[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image_name,
                    TextType.IMAGE,
                    image_url,
                )
            )
            original_text = updated_texts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    
def text_to_textnode(text):
    unique = set()
    nodes = [TextNode(text,'text')]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_images(nodes)
    return nodes 



text = "This is **text ** with an _italic_ word and a `code block` and an ![obi wan image](https: // i.imgur.com/fJRm4Vk.jpeg) and a[link](https: // boot.dev)"
print(text_to_textnode(text))
        
    

# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# node = TextNode(text, TextType.TEXT)
# print(split_nodes_images([node]))
# print(extract_markdown_images(text))


# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# print(new_nodes