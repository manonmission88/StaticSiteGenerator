import unittest
from text_delimitter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    ## Basic Formatting Tests ##

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_delim_unclosed_formatting(self):
        node = TextNode("This is **bold and _italic", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_multiple_formatting(self):
        node = TextNode("**bold** and _italic_ and `code`", TextType.TEXT)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_markdown_invalid_images(self):
        matches = extract_markdown_images("This is ![](https://img.com)")
        self.assertListEqual([], matches)

    def test_split_multiple_images(self):
        node = TextNode(
            "![img1](https://img1.com) and ![img2](https://img2.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://img1.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://img2.com"),
            ],
            new_nodes,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("link", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "[Google](https://google.com) and [Bing](https://bing.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Bing", TextType.LINK, "https://bing.com"),
            ],
            new_nodes,
        )

    def test_text_with_images_and_links(self):
        text = "Check this ![image](https://img.com) and [Google](https://google.com)"
        expected_output = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected_output)


    def test_malformed_markdown_link(self):
        node = TextNode("[bad link(https://example.com)", TextType.TEXT)  # Missing closing ]
        with self.assertRaises(ValueError) as context:
            split_nodes_links([node])
        self.assertEqual(str(context.exception), "Invalid markdown syntax for link")

    def test_malformed_markdown_image(self):
        node = TextNode("This is a ![bad image(https://example.com)", TextType.TEXT)  # Missing closing ]
        with self.assertRaises(ValueError) as context:
            split_nodes_images([node])
        self.assertEqual(str(context.exception), "Invalid markdown syntax for image")


    ## Full Markdown Conversion Tests ##

    def test_full_text_to_textnodes(self):
        text = "This is **bold** with _italic_ and `code`, ![img](https://img.com), and [link](https://link.com)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://img.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://link.com"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected_output)


if __name__ == "__main__":
    unittest.main()
