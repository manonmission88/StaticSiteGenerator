import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_props_to_html_with_no_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            None,
        )
        self.assertNotEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
        self.assertEqual(node.props_to_html(),None)
        
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()
