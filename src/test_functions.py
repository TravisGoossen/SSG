import unittest

from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image

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

    def test_split_link_two_links(self):
        node = TextNode("This text has a [link](https://www.google.com) in it. Here is a [second link](https://www.this.com)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" in it. Here is a ", TextType.NORMAL_TEXT),
                TextNode("second link", TextType.LINK, "https://www.this.com")
            ], 
            new_nodes
        )

    def test_split_link_empty_string(self):
        node = TextNode("", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])

    def test_split_link_5_links(self):
        node = TextNode("Please visit [site1](site1.com) and [site2](site2.com) and also [site3](site3.com).\
 Don't forget [site4](site4.com). The best of all is [site5](site5.com)", TextType.NORMAL_TEXT)  #The \ and new line continues the string on two lines
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Please visit ", TextType.NORMAL_TEXT),
                TextNode("site1", TextType.LINK, "site1.com"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("site2", TextType.LINK, "site2.com"),
                TextNode(" and also ", TextType.NORMAL_TEXT),
                TextNode("site3", TextType.LINK, "site3.com"),
                TextNode(". Don't forget ", TextType.NORMAL_TEXT),
                TextNode("site4", TextType.LINK, "site4.com"),
                TextNode(". The best of all is ", TextType.NORMAL_TEXT),
                TextNode("site5", TextType.LINK, "site5.com")
            ], new_nodes
        )

    def test_split_link_back_to_back(self):
        node = TextNode("This has [back](www.back.com)[to back](www.toBack.com)[links](www.b2b2bLinx.net)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has ", TextType.NORMAL_TEXT),
                TextNode("back", TextType.LINK, "www.back.com"),
                TextNode("to back", TextType.LINK, "www.toBack.com"),
                TextNode("links", TextType.LINK, "www.b2b2bLinx.net")
            ],
            new_nodes
        )
        
    def test_split_link_dont_return_empty_nodes(self):
        node = TextNode("[Welcome](www.image.com/Welcome) to the homepage [TravHome](www.TravHome.lieb)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Welcome", TextType.LINK, "www.image.com/Welcome"),
                TextNode(" to the homepage ", TextType.NORMAL_TEXT),
                TextNode("TravHome", TextType.LINK, "www.TravHome.lieb")
            ],
            new_nodes
        )

    def test_split_link_only_links(self):
        node = TextNode("[Only](only.com)[links](links.com)[here](here.com)[please!](please!.com)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Only", TextType.LINK, "only.com"),
                TextNode("links", TextType.LINK, "links.com"),
                TextNode("here", TextType.LINK, "here.com"),
                TextNode("please!", TextType.LINK, "please!.com")
            ],
            new_nodes
        )
        
    def test_split_link_multiple_nodes(self):
        node = TextNode("This is [node #1](www.bestNode.woo). Here is ano[ther one](www.therOne.hoo)", TextType.NORMAL_TEXT)
        node2 = TextNode("Lets try this with [more nodes!](www.MOREMOREMORE.mehr). Hofentlich funktioniert [es](www.Deutsch.lang)", TextType.NORMAL_TEXT)
        node3 = TextNode("Here is a [third](third.com) [node](node.com)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node, node2, node3])
        self.assertTrue(len(new_nodes) == 11)
        self.assertTrue(
            new_nodes[0].text_type == TextType.NORMAL_TEXT and 
            new_nodes[1].text_type == TextType.LINK and
            new_nodes[10].text_type == TextType.LINK)
        
    def test_split_link_empty_beginning(self):
        node = TextNode("   [first link](www.firstLink.com)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "www.firstLink.com")
            ],
            new_nodes
        )

   
    def test_split_image_node(self):
        node = TextNode("This text has an ![image](www.images.com/pic1)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "www.images.com/pic1")
            ],
            new_nodes
        )

    def test_split_3_images(self):
        node = TextNode("This ![lion](www.animalPics.net/lion) is scarier than this ![giraffe](www.animalPics.net/giraffe), but \
just as scary as this ![tiger](www.animalPics.net/tiger)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This ", TextType.NORMAL_TEXT),
                TextNode("lion", TextType.IMAGE, "www.animalPics.net/lion"),
                TextNode(" is scarier than this ", TextType.NORMAL_TEXT),
                TextNode("giraffe", TextType.IMAGE, "www.animalPics.net/giraffe"),
                TextNode(", but just as scary as this ", TextType.NORMAL_TEXT),
                TextNode("tiger", TextType.IMAGE, "www.animalPics.net/tiger")
            ],
            new_nodes
        )

    def test_split_images_b2b_images_multiple_nodes(self):
        node = TextNode("Here are three images: ![img1](img1.pic)![img2](img2.pic) ![img3](img3.pic)", TextType.NORMAL_TEXT)
        node2 = TextNode("![img4](img4.pic)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node, node2])
        # print(new_nodes)

    def test_split_images_none(self):
        node = TextNode("This has no images in it!", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has no images in it!", TextType.NORMAL_TEXT)
            ],
            new_nodes
        )

    def test_split_images_empty(self):
        node = TextNode("   ", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)


    def test_split_images_whitespace(self):
        node = TextNode("   ![first pic](www.firstPic.com) and... ![second pic](www.secPic.com)   ![third pic](www.thirdPic.com)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first pic", TextType.IMAGE, "www.firstPic.com"),
                TextNode(" and... ", TextType.NORMAL_TEXT),
                TextNode("second pic", TextType.IMAGE, "www.secPic.com"),
                TextNode("third pic", TextType.IMAGE, "www.thirdPic.com")
            ],
            new_nodes
        )

class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure

    def test_split_node_one_delimiter(self):
        node = TextNode("This text has _one delimiter", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        