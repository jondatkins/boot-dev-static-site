from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode
import re
from enum import Enum


def main():
    md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
    md_short = """
        This is **bolded** paragraph
        text in a p
        tag here

        """
    should_be_1 = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
    should_be = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>div>"

    print(f"1: {should_be_1}")
    node = markdown_to_html_node(md)
    # html = node.to_html()
    # print(node)
    if node is not None:
        html = node.to_html()
        print(f"2: {html}")


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# Split the markdown into blocks (you already have a function for this)
# Loop over each block:
#
#     Determine the type of block (you already have a function for this)
#     Based on the type of block, create a new HTMLNode with the proper data
#     Assign the proper child HTMLNode objects to the block node. I created
#     a shared text_to_children(text) function that works for all block types.
#     It takes a string of text and returns a list of HTMLNodes that represent
#     the inline markdown using previously created functions (think TextNode -> HTMLNode).
#     The "code" block is a bit of a special case: it should not do any inline markdown
#     parsing of its children. I didn't use my text_to_children function for this block
#     type, I manually made a TextNode and used text_node_to_html_node.
#
# Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # nodes = text_to_textnodes(block)
        # block = block.replace("\n", "")
        block_text = block.split("\n")

        block_text = list(map(str.strip, block_text))
        block = " ".join(block_text)
        if block_type is BlockType.PARAGRAPH:
            text_nodes = text_to_children(block)
            child_nodes = []
            paragraph_text = ""
            for node in text_nodes:
                if node.tag is not None:
                    child_nodes.append(node)
                    paragraph_text += node.to_html()
                else:
                    paragraph_text += node.value

            html_node = LeafNode("p", paragraph_text)
            html_nodes.append(html_node)
            # print(html_node)
        elif block_type is BlockType.HEADING:
            html_node = HTMLNode("p", [], {})
        elif block_type is BlockType.CODE:
            html_node = HTMLNode("p", [], {})
        elif block_type is BlockType.QUOTE:
            html_node = HTMLNode("p", [], {})
        elif block_type is BlockType.UNORDERED_LIST:
            html_node = HTMLNode("p", [], {})
        elif block_type is BlockType.ORDERED_LIST:
            html_node = HTMLNode("p", [], {})
    parent_html_node = ParentNode("div", html_nodes)
    return parent_html_node


#     It takes a string of text and returns a list of HTMLNodes that represent
#     the inline markdown using previously created functions (think TextNode -> HTMLNode).
def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(node.text_node_to_html_node())

    # print(nodes)
    return html_nodes


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        md_images = extract_markdown_images(old_node.text)
        if len(md_images) == 0:
            new_nodes.append(old_node)
            continue
        node_string = old_node.text
        for image in md_images:
            delim = f"![{image[0]}]({image[1]})"
            split_string = node_string.split(delim, 1)
            if len(split_string) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_string[0] != "":
                new_nodes.append(TextNode(split_string[0], TextType.TEXT))
            image_node = TextNode(image[0], TextType.IMAGE, image[1])
            new_nodes.append(image_node)
            node_string = split_string[1]
        if len(node_string) > 0:
            new_nodes.append(TextNode(node_string, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        md_links = extract_markdown_links(old_node.text)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue
        node_string = old_node.text
        for link in md_links:
            delim = f"[{link[0]}]({link[1]})"
            split_string = node_string.split(delim, 1)
            if len(split_string) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_string[0] != "":
                new_nodes.append(TextNode(split_string[0], TextType.TEXT))
            link_node = TextNode(link[0], TextType.LINK, link[1])
            new_nodes.append(link_node)
            node_string = split_string[1]
        if len(node_string) > 0:
            new_nodes.append(TextNode(node_string, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [
        TextNode(
            text,
            TextType.TEXT,
        )
    ]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


# def text_node_to_html_node(text_node):
#     if text_node.text_type is TextType.TEXT:
#         leaf_node = LeafNode(None, text_node.text)
#         return leaf_node
#     if text_node.text_type is TextType.BOLD:
#         leaf_node = LeafNode("b", text_node.text)
#         return leaf_node
#     if text_node.text_type is TextType.ITALIC:
#         leaf_node = LeafNode("i", text_node.text)
#         return leaf_node
#     if text_node.text_type is TextType.CODE:
#         leaf_node = LeafNode("code", text_node.text)
#         return leaf_node
#     if text_node.text_type is TextType.LINK:
#         leaf_node = LeafNode("a", text_node.text, {"href": text_node.url})
#         return leaf_node
#     if text_node.text_type is TextType.IMAGE:
#         leaf_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
#         return leaf_node
#


def markdown_to_blocks(markdown):
    split_strings = markdown.split("\n\n")
    trimmed_strings = [string.strip() for string in split_strings]
    while "" in trimmed_strings:
        trimmed_strings.remove("")
    return trimmed_strings


main()
