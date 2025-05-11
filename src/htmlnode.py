from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        html_string = ""
        for key in self.props:
            html_string += (f' {key}="{self.props[key]}"')
        return html_string
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return(f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})")

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode is missing 'value' attribute")
        if self.tag == None:
            return f"{self.value}"
        if not self.props:
            return(f"<{self.tag}>{self.value}</{self.tag}>")
        return(f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>")
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode is missing 'tag' attribute")
        if not self.children:
            raise ValueError("ParentNode is missing 'children' attribute")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        return(f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>")

    """
        When calling to_html on the parent node:
        1. create an empty string that will become the string of all of the children calling to_html on themselves
        2. Loop through each child of the parent node and call to_html on each of them
        3. concatenate each of the results of to_html on the children onto the empty string
        4. when it's gone through all of the children, return the full string
        5. Place the children string between the tags of the parent node and return that as the final html string
    """
        
    def __repr__(self):
        return(f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    
    