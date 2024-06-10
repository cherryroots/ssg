from typing import (
    List,
)

class HTMLNode():
    def __init__(self, tag:str = None, value:str = None, children:list = None, props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        return "".join(map(lambda key: f' {key}="{self.props[key]}"', self.props.keys()))

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag:str, value:str, props:dict=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:dict=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")
        
        if self.children == None or len(self.children) == 0:
            return ValueError("Invalid HTML: no children")
        
        output = ""
        for node in self.children:
            output += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{output}</{self.tag}>"
        
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"