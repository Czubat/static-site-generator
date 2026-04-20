from textnode import TextType, TextNode
from htmlnode import HTMLNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            chunks = node.text.split(delimiter)
            if len(chunks) % 2 == 0:
                raise Exception('Error: missing a closing delimiter')
        
            for i in range(len(chunks)):
                if chunks[i] == "":
                    continue  # optional: skip empty strings
                if i % 2 == 0:
                    new_nodes.append(TextNode(chunks[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(chunks[i], text_type))
    return new_nodes