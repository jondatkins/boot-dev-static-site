from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode
import re
from enum import Enum


def main():
    block_quote_md = """
> This is a
> blockquote block

this is paragraph text

"""
    block_quote_htmls = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
    # olist_md = "1. Item 1\n2. Item 2\n3. Item 3"
    # olist_html = "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"
    # <ul>
    #   <li>Coffee</li>
    #   <li>Tea</li>
    #   <li>Milk</li>
    # </ul>
    node = markdown_to_html_node(block_quote_md)
    test(block_quote_htmls, node.to_html())


def test(expected_html, generated_html):
    # print(expected_html)
    # print(generated_html)
    pass


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_strings = markdown.split("\n\n")
    trimmed_strings = [string.strip() for string in split_strings]
    while "" in trimmed_strings:
        trimmed_strings.remove("")
    return trimmed_strings


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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def markdown_to_html_node_mine(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # nodes = text_to_textnodes(block)
        # block = block.replace("\n", "")
        if block_type is BlockType.PARAGRAPH:
            block_text = block.split("\n")
            block_text = list(map(str.strip, block_text))
            block = " ".join(block_text)
            child_nodes = text_to_children(block)
            paragraph_node = ParentNode("p", child_nodes)
            html_nodes.append(paragraph_node)
        elif block_type is BlockType.HEADING:
            header_text = block.replace("#", "")
            child_nodes = text_to_children(header_text)
            num_hashes = 0
            for char in block:
                if char == "#":
                    num_hashes += 1
            heading_node = ParentNode(f"h{num_hashes}", child_nodes)
            html_nodes.append(heading_node)
        elif block_type is BlockType.CODE:
            block = block.replace("```", "")
            block = block.lstrip("\n")
            code_node = LeafNode("code", block)
            pre_node = ParentNode("pre", [code_node], {})
            html_nodes.append(pre_node)
        elif block_type is BlockType.QUOTE:
            # remove angle bracket
            quote_text = block[1:]
            # remove white space
            quote_text = quote_text.lstrip()
            child_nodes = text_to_children(quote_text)
            quote_node = ParentNode("blockquote", child_nodes)
            html_nodes.append(quote_node)
        elif block_type is BlockType.UNORDERED_LIST:
            block = block.replace("-", "")
            list_items = block.split("\n")
            li_nodes = []
            for item in list_items:
                item = item.strip()
                child_nodes = text_to_children(item)
                li_nodes.append(ParentNode("li", child_nodes))
            ul_node = ParentNode("ul", li_nodes)
            html_nodes.append(ul_node)
        elif block_type is BlockType.ORDERED_LIST:
            block = block.replace("-", "")
            list_items = block.split("\n")
            li_nodes = []
            for item in list_items:
                # remove '1. 2. etc' from start of string
                item = item[2:]
                item = item.strip()
                child_nodes = text_to_children(item)
                li_nodes.append(ParentNode("li", child_nodes))
            ul_node = ParentNode("ol", li_nodes)
            html_nodes.append(ul_node)
    parent_html_node = ParentNode("div", html_nodes)
    return parent_html_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        child_nodes.append(text_node.text_node_to_html_node())

    return child_nodes


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    # Get the text minus the hashes
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    # Remember to raise errors for invalid text
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    # Strip the first 3 backticks and newline, and the last three backticks
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = raw_text_node.text_node_to_html_node()
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        # The list starts with e.g. '1. ', so split on '. ' once only
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        # The first chars should be '- ', so remove these
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


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


main()
