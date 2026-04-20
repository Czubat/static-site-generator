from textnode import TextType

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        output = ""
        if self.props == None:
            return output
        for prop in self.props:
            output += f" {prop}=\"{self.props[prop]}\""
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node does not have a value")
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
        
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError('tag cannont be None')
        if self.children == None:
            raise ValueError('parent must have children')
        
        child_string = ""
        for child in self.children:
            child_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    # TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    # TextType.BOLD: This should return a LeafNode with a "b" tag and the text
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text )
    
    # TextType.ITALIC: "i" tag, text
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    
    # TextType.CODE: "code" tag, text
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    
    # TextType.LINK: "a" tag, anchor text, and "href" prop
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    
    # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    
    else:
        raise Exception('unknown type')