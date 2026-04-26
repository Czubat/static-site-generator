from enum import Enum
from functions import text_to_textnodes
from htmlnode import text_node_to_html_node, ParentNode
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE ="quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            cleaned_blocks.append(block)
    return cleaned_blocks

def block_to_block_type(input):
    starting_char = input[0]
    
    if starting_char == '#':
        for index in range(1,7):
            if input[index] == ' ':
                return BlockType.HEADING
            if input[index] == '#':
                if index < 6:
                    continue
                else:
                    return BlockType.PARAGRAPH
            else:
                return BlockType.PARAGRAPH

    elif starting_char == '`':
        if input[0:4] == "```\n" and input[-3:] == "```":
            return BlockType.CODE
        else:
            return BlockType.PARAGRAPH
        
    elif starting_char == '>':
        split_lines = input.split('\n')
        for line in split_lines:
            if line.startswith('>'):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    elif starting_char == '-':
        split_lines = input.split('\n')
        for line in split_lines:
            if line.startswith('- '):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    elif starting_char == '1':
        split_lines = input.split('\n')
        for index in range(0, len(split_lines)):
            if split_lines[index].startswith(f"{index + 1}. "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break
                if level + 1 >= len(block):
                    raise ValueError(f"invalid heading level: {level}")
                text = block[level + 1:]   # skip "#'s"
                children = text_to_children(text)
                nodes.append(ParentNode(f"h{level}", children))

            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p", text_to_children(" ".join(block.split('\n')))))
            
            case BlockType.CODE:
                # strip leading ``` and trailing ```
                text = block[4:-3]   # think about why these specific indices
                raw_text_node = TextNode(text, TextType.TEXT)
                code_child = text_node_to_html_node(raw_text_node)
                code_node = ParentNode("code", [code_child])
                nodes.append(ParentNode("pre", [code_node]))
            
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                children = text_to_children(content)
                nodes.append(ParentNode("blockquote", children))
                
            case BlockType.ULIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[2:]   # skip "- "
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                nodes.append(ParentNode("ul", html_items))
            
            case BlockType.OLIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item.split(' ', maxsplit=1)[1]   # skip "X.  "
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                nodes.append(ParentNode("ol", html_items))


    return ParentNode('div', nodes)