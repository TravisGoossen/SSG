import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from functions import split_nodes_delimiter

class TestFunctions(unittest.TestCase):
    node = TextNode("This is a `code block` word.", TextType.NORMAL_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
    print(new_nodes)