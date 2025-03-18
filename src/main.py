import sys
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_html_node
import os 
import shutil

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'  # Get basepath from CLI or default to '/'
    static_to_public(src, dest)
    generate_pages_recursive(from_path, template_path, to_path, basepath)


def static_to_public(src,dest):
    '''
    moving files from one directory(static) to other (public)
    
    '''
    if not os.path.exists(dest):
        os.makedirs(dest)

    # Remove all existing content from dest before copying
    for item in os.listdir(dest):
        item_path = os.path.join(dest, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove entire directory
        else:
            os.remove(item_path)
                
    for item in os.listdir(src):
        src_path = os.path.join(src,item)
        dest_path = os.path.join(dest,item)
        if os.path.isdir(src_path):
            #copied all the nested directories 
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)  
        else:
            shutil.copy2(src_path,dest_path)
            
def extract_title(markdown):
    updated_markdown = markdown.split('\n')
    for line in updated_markdown:
        if line.startswith('#'):
            return line[1:]
    return ''
        

def generate_page(from_path,template_path,dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")
    with open(from_path, 'r', encoding="utf-8") as file:
        markdown_content = file.read()
    with open(template_path, 'r', encoding="utf-8") as file:
        template_content = file.read()
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace('{{ Title }}', title)
    template_content = template_content.replace('{{ Content }}', html_content)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(template_content)
        
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isdir(file_path):  #directory -- recurse 
            sub_dest_dir = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(file_path, template_path, sub_dest_dir, basepath)
        elif filename.endswith(".md"):  # Process only markdown files
            output_path = os.path.join(dest_dir_path, filename.replace(".md", ".html"))
            generate_page(file_path, template_path, output_path, basepath)
        # Ignore non-markdown files
        

if __name__ == "__main__":
    src = './static'
    dest = './public'
    from_path = './content/'
    template_path = './template.html'
    to_path = './public'
    main()
