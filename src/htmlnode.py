class HTMLNode:
    """
    This class represents an HTML node with a tag, content, children, and properties.
    """
    def __init__(self,tag=None,value=None, children=None, props=None): # optional
        self.tag = tag 
        self.value = value 
        self.children = children 
        self.props = props 
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        
        """
        string that represents the HTML attributes of the node.
        
        """
        if self.props is None:
            return None 
        final_output = ""
        for key, value in self.props.items():
            final_output += f" {key}=\"{value}\""
        return final_output 
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    
            