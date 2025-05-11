import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_link_type_eq(self):
        node = TextNode("URL testing node", TextType.LINK, "www.linkMe.org")
        node2 = TextNode("URL testing node 2", TextType.LINK, "www.imLinkedUp.net")
        self.assertEqual(node.text_type, node2.text_type)

    def test_url_none_eq(self):
        node = TextNode("URL None node", TextType.NORMAL_TEXT)
        node2 = TextNode("URL not None node", TextType.LINK, "www.linkMe.org")
        node3 = TextNode("URL None node", TextType.NORMAL_TEXT)
        if node.url == None and node3.url == None:
            self.assertEqual(node.url, node3.url)
        else:
            self.assertEqual(node.url, node3.url)

    def test_text_is_different(self):
        node = TextNode("Testing text number 1", TextType.NORMAL_TEXT)
        node2 = TextNode("Testing text number 15", TextType.ITALIC_TEXT)
        self.assertNotEqual(node.text, node2.text)

    def test_if_text_exists(self):
        node = TextNode("asd", TextType.LINK)
        if node.text_type == TextType.IMAGE:
            print("\nTesting if text exists in non-image types")
            print("Text Type is an image and may not require text, therefore passes test")
            self.assertEqual(1, 1)
        if node.text == "":
            self.assertEqual(1, 0)
        else:
            self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()