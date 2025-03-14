from textnode import TextNode, TextType
from enum import Enum

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
        print(updated_words)
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
        

node = TextNode("This is text with a ``code block** word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
print(new_nodes)