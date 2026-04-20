from textnode import TextNode, TextType
from functions import split_nodes_delimiter

def main():
    # text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node)
    node = TextNode("Hello `world`` friend", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    for n in result:
        print(n)

main()