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

# text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))

# node = TextNode("This is text with a ``code block** word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# print(new_nodes