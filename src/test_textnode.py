import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a node", text_type_text)
        node2 = TextNode("This is a node", text_type_bold)
        node3 = TextNode("This is a node", text_type_image, url="https://test.com/image.jpg")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node, node3)

    def test_url_eq(self):
        node = TextNode("This is an image node", text_type_image, url="https://test.com/image.jpg")
        node2 = TextNode("This is an image node", text_type_image, url="https://test.com/image.jpg")
        self.assertEqual(node, node2)

    def test_url_ineq(self):
        node = TextNode("This is an image node", text_type_image, url="https://test.com/image.jpg")
        node2 = TextNode("This is an image node", text_type_image, url="https://test.com/image2.jpg")
        self.assertNotEqual(node, node2)

    def test_link_not_url(self):
        node = TextNode("This is a node", text_type_image, url="https://test.com/image.jpg")
        node2 = TextNode("This is a node", text_type_link, url="https://test.com/image.jpg")
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold, url=None)
        node3 = TextNode("This is a text node", text_type_bold, url="None")
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node, node3)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
        
if __name__ == "__main__":
    unittest.main()
