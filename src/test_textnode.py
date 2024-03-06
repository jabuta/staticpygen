from textnode import TextNode
import unittest

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1,node2)

    def test_uneq_nodes(self):
        node1 = TextNode("Hello", "Type1", "example.com")
        node2 = TextNode("World", "Type2", "example.org")
        self.assertNotEqual(node1, node2)

    def test_diff_class(self):
        node = TextNode("Hello", "Type1", "example.com")
        other = "Hello"
        self.assertNotEqual(node, other)

    def test_none_values(self):
        node1 = TextNode(None, None, None)
        node2 = TextNode(None, None, None)
        self.assertEqual(node1, node2)

    def test_partial_none_values(self):
        node1 = TextNode("Hello", None, "example.com")
        node2 = TextNode("Hello", None, "example.com")
        self.assertEqual(node1, node2)

    def test_different_none_values(self):
        node1 = TextNode("Hello", None, "example.com")
        node2 = TextNode("Hello", "None", "example.com")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()