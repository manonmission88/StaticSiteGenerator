from htmlnode import HTMLNode
from leafnode import LeafNode

'''
child class of HtmlNode class 
'''
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=children,props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError('tag is required')
        if not self.children:
            raise ValueError('children is required')
        final_html = f'<{self.tag}>'
        for children in self.children:
            final_html += children.to_html()
        return final_html + f'</{self.tag}>'


# child_node = LeafNode("span", "child",{'a':'test.com'})
# parent_node = ParentNode("div", [child_node])
# print(parent_node.to_html())
        
        
        