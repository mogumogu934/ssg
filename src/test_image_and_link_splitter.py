import unittest
from textnode import TextNode, TextType
from image_and_link_splitter import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestImageAndLinkSplitter(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rice ball](https://i.imgur.com/aYa0qHh.jpeg) and ![okayu](https://i.imgur.com/uIA2Kat.gif)"
        result = extract_markdown_images(text)
        expected = [("rice ball", "https://i.imgur.com/aYa0qHh.jpeg"), ("okayu", "https://i.imgur.com/uIA2Kat.gif")]
        self.assertEqual(result, expected)
        
    def test_extract_markdown_links(self):
        text = "This is text with a link [to okayu](https://www.okayu.nyaa) and [to youtube](https://www.youtube.com)"
        result = extract_markdown_links(text)
        expected = [("to okayu", "https://www.okayu.nyaa"), ("to youtube", "https://www.youtube.com")]
        self.assertEqual(result, expected)
        
    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("Check out this ![cool image](https://www.i.imgur.com/coolimage.png)! Isn't it cool?", TextType.TEXT),
            TextNode("![okayu](https://www.i.imgur.com/okayu.gif)", TextType.TEXT),
            TextNode("These are my favorite characters: ![sakuya](https://www.i.imgur.com/sakuya.jpeg) and ![remilia](https://www.i.imgur.com/remilia.png)", TextType.TEXT),
            TextNode("Look at this ![](https://www.i.imgur.com/fluffycat.jpeg)", TextType.TEXT),
            TextNode("Just text", TextType.TEXT),
        ]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("cool image", TextType.LINK, "https://www.i.imgur.com/coolimage.png"),
            TextNode("! Isn't it cool?", TextType.TEXT),
            TextNode("okayu", TextType.LINK, "https://www.i.imgur.com/okayu.gif"),
            TextNode("These are my favorite characters: ", TextType.TEXT),
            TextNode("sakuya", TextType.LINK, "https://www.i.imgur.com/sakuya.jpeg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("remilia", TextType.LINK, "https://www.i.imgur.com/remilia.png"),
            TextNode("Look at this ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.i.imgur.com/fluffycat.jpeg"),
            TextNode("Just text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("Check out this [cool image](https://www.i.imgur.com/coolimage.png)! Isn't it cool?", TextType.TEXT),
            TextNode("[okayu](https://www.i.imgur.com/okayu.gif)", TextType.TEXT),
            TextNode("These are my favorite characters: [sakuya](https://www.i.imgur.com/sakuya.jpeg) and [remilia](https://www.i.imgur.com/remilia.png)", TextType.TEXT),
            TextNode("Look at this [](https://www.i.imgur.com/fluffycat.jpeg)", TextType.TEXT),
            TextNode("Just text", TextType.TEXT),
        ]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("cool image", TextType.LINK, "https://www.i.imgur.com/coolimage.png"),
            TextNode("! Isn't it cool?", TextType.TEXT),
            TextNode("okayu", TextType.LINK, "https://www.i.imgur.com/okayu.gif"),
            TextNode("These are my favorite characters: ", TextType.TEXT),
            TextNode("sakuya", TextType.LINK, "https://www.i.imgur.com/sakuya.jpeg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("remilia", TextType.LINK, "https://www.i.imgur.com/remilia.png"),
            TextNode("Look at this ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.i.imgur.com/fluffycat.jpeg"),
            TextNode("Just text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
