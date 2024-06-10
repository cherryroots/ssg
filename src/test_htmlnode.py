import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        node_a = HTMLNode("a", props={"href": "https://www.google.com", "target": "_blank"})
        node_p = HTMLNode("p", "Hello, world!")
        self.assertEqual(
            " href=\"https://www.google.com\" target=\"_blank\"", node_a.props_to_html()
        )
        self.assertEqual(
            "", node_p.props_to_html()
        )

    def test_to_html_props(self):
        node_p = LeafNode("p", "This is a paragraph of text.")
        node_a = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            "<a href=\"https://www.google.com\">Click me!</a>", node_a.to_html()
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_many_children(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )   
        html="<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), html)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()