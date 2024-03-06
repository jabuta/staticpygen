class TextNode:
    def __new__(cls, TEXT=None, TYPE=None, URL=None):
        instance = super().__new__(cls)
        return instance

    def __init__(self, TEXT=None, TYPE=None, URL=None):
        self.text = TEXT
        self.type = TYPE
        self.url = URL

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text == other.text and
                self.type == other.type and
                self.url == other.url
            )
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"