import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link

class TestFunctions(unittest.TestCase):

    def test_split_node_already_bold(self):
        node = TextNode("This is already bold and should not be adjusted", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_split_node_code(self):
        node = TextNode("This is a `code block` word.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(len(new_nodes), 3)

    def test_split_node_italic(self):
        node = TextNode("This is _italic_ text.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertTrue(new_nodes[0].text_type == TextType.NORMAL_TEXT and new_nodes[1].text_type == TextType.ITALIC_TEXT)

    def test_split_node_bold(self):
        node = TextNode("This is some **bold** text.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertTrue(new_nodes[0].text_type == TextType.NORMAL_TEXT and new_nodes[1].text_type == TextType.BOLD_TEXT)

    def test_extract_images(self):
        text = "This is some text with a ![Test Image](https://test.images.com/1Plp31TestImage)"
        self.assertListEqual([("Test Image", "https://test.images.com/1Plp31TestImage")], extract_markdown_images(text))

    def test_extract_images_multiple(self):
        text = "Take a look at this ![April sales chart](https://www.charts.net/sales123456) and compare it with ![May sales chart](https://www.charts.net/sales11231115)"
        self.assertIn(
            ('April sales chart', 'https://www.charts.net/sales123456') and ('May sales chart', 'https://www.charts.net/sales11231115'),
              extract_markdown_images(text))
        self.assertEqual(2, len(extract_markdown_images(text)))

    def test_extract_images_none(self):
        text = "This text contains no images at all!"
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_links(self):
        text = "This link sends you to [Lady Gaga's website](https://www.LadyGaga.com)"
        self.assertListEqual([("Lady Gaga's website", "https://www.LadyGaga.com")], extract_markdown_links(text))

    def test_extract_links_multiple(self):
        text = "I'm going to send you to [Youtube](https://www.youtube.com) and [Google](https://www.google.com) to find those answers"
        self.assertIn(
            ('Youtube', 'https://www.youtube.com') and ('Google', 'https://www.google.com'), 
            extract_markdown_links(text)
        )

    def test_extract_links_none(self):
        text = "This text contains no links at all!"
        self.assertListEqual([], extract_markdown_links(text))

    def test_split_link(self):
        node = TextNode("This text has a [link](https://www.google.com)", TextType.NORMAL_TEXT)
        print(split_nodes_link([node]))

class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure

    def test_split_node_one_delimiter(self):
        node = TextNode("This text has _one delimiter", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        