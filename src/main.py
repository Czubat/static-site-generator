from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images

def main():
    # text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node)
    
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

main()