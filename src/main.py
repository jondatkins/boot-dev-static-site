from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


def main():
    # text_node = TextNode(
    #     "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    # )
    # print(text_node)
    # node = HTMLNode("a", "a tag", [], {"href": "https://www.google.com"})
    # print(node.props_to_html())
    # leaf_node = LeafNode("p", "This is a paragraph of text.").to_html()
    # "<p>This is a paragraph of text.</p>"
    # print(leaf_node.to_html())
    # node = LeafNode("p", "Hello, world!")
    # print(node.to_html())  # "<p>Hello, world!</p>"
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(node.to_html())
    print("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


if __name__ == "__main__":
    main()
