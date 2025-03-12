from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag=tag,value=value,props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value 
        if self.props:
            html = self.props_to_html()
            return f"<{self.tag}{html}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
            
    