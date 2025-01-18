from enum import Enum
from textnode import TextType, TextNode

def main():
    textnode_test = TextNode("This is a text node", TextType.BOLD, "https://www.textnode.net")
    print(textnode_test)

main()
