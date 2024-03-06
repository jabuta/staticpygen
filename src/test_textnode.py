import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class SplitNodesDelimiterTests(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiter(self):
        node = TextNode("This is just a regular text.", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_invalid_syntax(self):
        node = TextNode("This is an *unclosed italic word.", text_type_text)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: unclosed delimiter")


if __name__ == "__main__":
    unittest.main()