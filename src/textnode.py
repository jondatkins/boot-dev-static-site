from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text} {self.text_type.value} {self.url})"

    def text_node_to_html_node(self, text_node):
        if text_node.text_type is TextType.TEXT:
            leaf_node = LeafNode(None, text_node.text)
            return leaf_node
        if text_node.text_type is TextType.BOLD:
            leaf_node = LeafNode("b", text_node.text)
            return leaf_node
        if text_node.text_type is TextType.ITALIC:
            leaf_node = LeafNode("i", text_node.text)
            return leaf_node
        if text_node.text_type is TextType.CODE:
            leaf_node = LeafNode("code", text_node.text)
            return leaf_node
        if text_node.text_type is TextType.LINK:
            leaf_node = LeafNode("a", text_node.text, {"href": text_node.url})
            return leaf_node
        if text_node.text_type is TextType.IMAGE:
            leaf_node = LeafNode(
                "img", "", {"src": text_node.url, "alt": text_node.text}
            )
            return leaf_node
