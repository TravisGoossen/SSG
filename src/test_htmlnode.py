import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    # All tests in this class are expected to PASS. If they pass the test, it is a success

    def test_props_to_html_type(self):
        node = HTMLNode("<p>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        if type(node.props_to_html()) == str:
            # String type returned
            self.assertEqual(1, 1)
        else: 
            # Non-string type returned
            self.assertEqual(1, 0)

    def test_repr_method(self):
        node = HTMLNode("<p>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), "HTMLNode(<p>, None, None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_has_props(self):
        node = HTMLNode("<h1>", "Testing Header 1 Text Here", None, {"class": "Bold", "name": "first_header"})
        if node.props:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)

    def test_leaf_node(self):
        node = LeafNode("p", "This is a paragraph example")
       # print(f"TEST leaf node ::: {node}")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "testing Text to HTML").to_html()
        self.assertEqual(node, "testing Text to HTML")
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Testing paragraph text")
        self.assertEqual(node.to_html(), "<p>Testing paragraph text</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link test", {"href": "https://www.youtube.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.youtube.com">This is a link test</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a header")
        self.assertEqual(node.to_html(), '<h1>This is a header</h1>')

    def test_parent_to_html_leaf_children_props(self):
        node = ParentNode(
            "p",
             [
                 LeafNode("h1", "This is an h1 text"),
                 LeafNode("b", "This is bold"),
                 LeafNode(None, "Normal text")
             ],
             {"class": "center bold"})
        self.assertEqual(
                node.to_html(),
                '<p class="center bold"><h1>This is an h1 text</h1><b>This is bold</b>Normal text</p>'
              )

    def test_parent_to_html_with_multiple_children(self):
        child_node_1 = LeafNode("h1", "H1 testing text", {"name": "Main H1", "class": "center"})
        child_node_2 = LeafNode("span", "Span testing node")
        parent_node = ParentNode("body", [child_node_1, child_node_2], {"class": "body-style"})
        self.assertEqual(
            parent_node.to_html(),
            '<body class="body-style"><h1 name="Main H1" class="center">H1 testing text</h1><span>Span testing node</span></body>'
        )

    def test_parent_to_html_with_grandchildren(self):
        grandchild = LeafNode("p", "This is a child")
        child = ParentNode("div", [grandchild])
        Parent = ParentNode("body", [child])
        self.assertEqual(
            Parent.to_html(),
            '<body><div><p>This is a child</p></div></body>'
        )

    def test_text_to_html_normal(self):
        node = TextNode("Text node testing", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Text node testing")

    def test_text_to_html_italic(self):
        node = TextNode("Italic node testing", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic node testing")

class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure
        
    #All tests in this class are expected to FAIL. If they fail, that is a successful test.
        
    def test_parent_to_html_no_children(self): 
        parent = ParentNode("head").to_html()

if __name__ == "__main__":
    unittest.main()