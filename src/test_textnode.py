import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.BOLD, 'http')
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

    def test_empty_string(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_same_type_different_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("World", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_same_text_different_type(self):
        node = TextNode("Sample", TextType.BOLD)
        node2 = TextNode("Sample", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_with_and_without_link(self):
        node = TextNode("Text", TextType.BOLD, "http://example.com")
        node2 = TextNode("Text", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
