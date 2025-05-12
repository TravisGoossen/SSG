from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from functions import *

def main():
    testObj = TextNode("Testing", "text")
    testObj2 = TextNode("URL test", "link", "https://www.youtube.com")
    testObj3 = TextNode("Testing", "text")
    print(testObj)
    print(testObj2)

main()