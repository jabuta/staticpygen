from htmlnode import LeafNode


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

    def __eq__(self, other) -> bool:
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html_node(self) -> LeafNode:
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