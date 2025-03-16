def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    filtered_markdown = []
    for block in blocks:
        if len(block) == 0:
            continue
        block = block.strip()
        filtered_markdown.append(block)
    return filtered_markdown


text = """# This is a heading

This is a paragraph of text. 
It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
print(markdown_to_blocks(text))
