from textnode import TextNode, TextType
import re
from enum import Enum


def main():
    heading = "# A heading"
    not_heading = "#Not a heading"
    not_heading_2 = "# Not a heading"
    code = "``` foobar ```"
    quote = "> foobar foo bar"
    not_a_quote = ">a quote"
    unordered_list = "- item x\n- item y"
    not_unordered_list = "-item x\n- item y"
    ordered_list = "1. List Item 1\n2. List Item 2"
    not_ordered_list = "1. List Item 1\n2.List Item 2"

    code_2 = "```\n print('foo')\n ```"
    # print(block_to_block_type(not_a_quote))


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block_text):
    heading_pattern = r"^(#{1,6}) ([^\r\n]*)\r?$"
    code_pattern = r"```[\s\S]*?```"
    quote_pattern = r"> .+"
    unordered_list_pattern = r"- (.+)"
    ordered_list_pattern = r"[0-9]{0,9}\. (.+)"
    if re.search(heading_pattern, block_text):
        return BlockType.HEADING
    elif re.search(code_pattern, block_text):
        return BlockType.CODE
    elif re.search(quote_pattern, block_text):
        return BlockType.QUOTE
    elif re.search(unordered_list_pattern, block_text):
        lines = block_text.split("\n")
        for line in lines:
            if not re.search(unordered_list_pattern, line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif re.search(ordered_list_pattern, block_text):
        lines = block_text.split("\n")
        for line in lines:
            if not re.search(ordered_list_pattern, line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_block_type_course(block):
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
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
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


def markdown_to_blocks(markdown):
    split_strings = markdown.split("\n\n")
    trimmed_strings = [string.strip() for string in split_strings]
    while "" in trimmed_strings:
        trimmed_strings.remove("")
    return trimmed_strings


main()
