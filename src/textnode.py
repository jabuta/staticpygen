from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text: str, text_type: str, url: str =None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html_node(self):
        if self.text_type == text_type_text:
            return LeafNode(value=self.text)
        if self.text_type == text_type_bold:
            return LeafNode(tag="b", value=self.text)
        if self.text_type == text_type_italic:
            return LeafNode(tag="i", value=self.text)
        if self.text_type == text_type_code:
            return LeafNode(tag="code", value=self.text)
        if self.text_type == text_type_link:
            return LeafNode(tag="a", value=self.text, props={'href': self.url})
        if self.text_type == text_type_image:
            return LeafNode(tag="img", value="", props={'src': self.url, 'alt': self.text})
        raise ValueError("invalid text type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_strings = old_node.text.split(delimiter)
        if len(split_strings) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: unclosed delimiter")
        for i in range(0,len(split_strings)):
            if i % 2 == 0:
                curr_node = TextNode(split_strings[i], text_type_text)
                new_nodes.append(curr_node)
            else:
                curr_node =TextNode(split_strings[i], text_type)
                new_nodes.append(curr_node)
    return new_nodes

def extract_markdown_images(text: str):
    return re.findall( r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_URLs(text: str):
    return re.findall( r"(?<!\!)\s*\[(.*?)\]\((.*?)\)", text)
