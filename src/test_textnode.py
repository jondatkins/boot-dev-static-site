import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # def test_eq(self):
    #     node = TextNode("This is a text node", TextType.BOLD)
    #     node2 = TextNode("This is a text node", TextType.BOLD)
    #     self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.text_node_to_html_node(node)
        if html_node is not None:
            self.assertEqual(html_node.tag, "b")
            self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = node.text_node_to_html_node(node)
        if html_node is not None:
            self.assertEqual(html_node.tag, "i")
            self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = node.text_node_to_html_node(node)
        if html_node is not None:
            self.assertEqual(html_node.tag, "code")
            self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = node.text_node_to_html_node(node)

        # print(f"LINK NODE: {html_node}")
        if html_node is not None:
            self.assertEqual(html_node.tag, "a")
            self.assertEqual(html_node.value, "Click me!")
            self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_image(self):
        node = TextNode("foo bar", TextType.IMAGE, "foo/bar")
        html_node = node.text_node_to_html_node(node)
        # print(f"IMAGE NODE: {html_node}")
        if html_node is not None:
            self.assertEqual(html_node.tag, "img")
            self.assertEqual(html_node.value, "")
            self.assertEqual(html_node.props["src"], "foo/bar")
            self.assertEqual(html_node.props["alt"], "foo bar")


if __name__ == "__main__":
    unittest.main()
