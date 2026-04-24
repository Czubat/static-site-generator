from textnode import TextType, TextNode
import re

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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_images = extract_markdown_images(node.text)
            if not extracted_images:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for image in extracted_images:
                    split = remaining_text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
                    if split[0] != "":
                        new_nodes.append(TextNode(split[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    remaining_text = split[1]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_links = extract_markdown_links(node.text)
            if not extracted_links:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for link in extracted_links:
                    split = remaining_text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
                    if split[0] != "":
                        new_nodes.append(TextNode(split[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    remaining_text = split[1]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            cleaned_blocks.append(block)
    return cleaned_blocks