from textnode import TextNode, TextType
import re


def main():
    test_string_1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    test_string_2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and also [to reddit](https://www.reddit.com)"
    test_string_3 = "This is text with a link [to boot dev](https://www.boot.dev)"
    test_string_4 = "This is text with a link [to boot dev](https://www.boot.dev) followed by more text"
    test_string_5 = "This is text with a link [to boot dev](https://www.boot.dev) followed by more text [to boot dev](https://www.boot.dev) and so on"
    test_string_6 = "[to boot dev](https://www.boot.dev) The link is at the start."
    #
    node = TextNode(
        test_string_4,
        TextType.TEXT,
    )
    #
    # node_2 = TextNode(
    #     test_string_2,
    #     TextType.TEXT,
    # )
    # split_strings = node_2.text.split("[to boot dev](https://www.boot.dev)", 1)
    # print(split_strings)

    new_nodes = split_nodes_link([node])
    print(new_nodes)
    # [
    #     TextNode("This is text with a link ", TextType.TEXT),
    #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #     TextNode(" and ", TextType.TEXT),
    #     TextNode(
    #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #     ),
    # ]


def split_nodes_delimiter_mine(old_nodes, delimiter, text_type):
    split_strings = []
    new_nodes = []
    non_text_node_text = ""
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiter_positions = []
            for i in range(1, len(node.text)):
                if text_type == TextType.CODE or text_type == TextType.ITALIC:
                    if node.text[i - 1] == delimiter:
                        delimiter_positions.append(i - 1)
                else:
                    if node.text[i - 1] + node.text[i] == delimiter:
                        delimiter_positions.append(i)
            if len(delimiter_positions) != 2:
                raise Exception("Invalid Markdown for " + node.text)
            non_text_node_text = node.text[
                delimiter_positions[0] + 1 : delimiter_positions[1]
            ]
            split_string_list = node.text.split(delimiter)
            split_strings.extend(split_string_list)
        for text in split_strings:
            if text not in non_text_node_text:
                text_node = TextNode(text, TextType.TEXT)
                new_nodes.append(text_node)
            else:
                text_node = TextNode(text, text_type)
                new_nodes.append(text_node)
    return new_nodes


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


# Create a function extract_markdown_images(text) that takes
# raw markdown text and returns a list of tuples. Each tuple
# should contain the alt text and the URL of any markdown images
def extract_markdown_images_old(text):
    select_in_square_brackets = r"(?<=\!\[).+?(?=\])"
    select_url_in_round_brackets = r"(?<=\()(https:?\/\/.*?)(?=\))"
    alt_regex = r"\!\[[\w\s]+\]"
    url_regex = r"\(https?:\/\/.*?\)"
    regex = alt_regex + url_regex
    image_info = re.findall(regex, text)

    alt_and_url = []
    for image in image_info:
        alt = re.findall(select_in_square_brackets, image)[0]
        url = re.findall(select_url_in_round_brackets, image)[0]
        alt_and_url.append((alt, url))
    return alt_and_url


def extract_markdown_links_old(text):
    select_in_square_brackets = r"(?<=\[).+?(?=\])"
    select_url_in_round_brackets = r"(?<=\()(https:?\/\/.*?)(?=\))"
    link_title_regex = r"\[[\w\s]+\]"
    url_regex = r"\(https?:\/\/.*?\)"
    regex = link_title_regex + url_regex
    link_info = re.findall(regex, text)

    alt_and_url = []
    for image in link_info:
        link_text = re.findall(select_in_square_brackets, image)[0]
        url = re.findall(select_url_in_round_brackets, image)[0]
        alt_and_url.append((link_text, url))
    return alt_and_url


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
        md_images = extract_markdown_images(old_node.text)
        print(md_images)


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        md_links = extract_markdown_links(old_node.text)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue
        elif len(md_links) == 1:
            delimiter = f"[{md_links[0][0]}]({md_links[0][1]})"
            split_string = old_node.text.split(delimiter, 1)

        else:
            delimiters = []
            for tup in md_links:
                delim = f"[{tup[0]}]({tup[1]})"
                delimiters.append(delim)
            text_strings = []
            node_string = old_node.text
            for delim in delimiters:
                split_string = node_string.split(delim, 1)
                text_strings.append(split_string[0])
                node_string = split_string[1:][0]

    return new_nodes


main()
