"""
It takes a raw Markdown string (representing a full document) 
as input and returns a list of "block" strings.

"""
from enum import Enum 
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
    
    
    
    
    
    
text = """# This is a heading

This is a paragraph of text. 
It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
# markdown_blocks = markdown_to_blocks(text)
# for block in markdown_blocks:
#     print(block,block_to_block_type(block))
