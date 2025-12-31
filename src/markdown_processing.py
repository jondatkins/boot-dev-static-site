from textnode import TextNode, TextType
import re


def main():
    test_string_1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    test_string_2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and also [to reddit](https://www.reddit.com)"
    test_string_3 = "This is text with a link [to boot dev](https://www.boot.dev)"
    test_string_4 = "This is text with a link [to boot dev](https://www.boot.dev) followed by more text"
    test_string_5 = "This is text with a link [to boot dev](https://www.boot.dev) followed by more text [to boot dev](https://www.boot.dev) and so on"
    test_string_6 = "[to boot dev](https://www.boot.dev) The link is at the start."
    test_string_7 = "The link is at the end [to boot dev](https://www.boot.dev)"
    test_string_8 = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #
    node = TextNode(
        test_string_1,
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
        md_images = extract_markdown_images(old_node.text)
        print(md_images)


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        md_links = extract_markdown_links(old_node.text)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue
        # There is only one link in the old node
        elif len(md_links) == 1:
            delimiter = f"[{md_links[0][0]}]({md_links[0][1]})"
            split_string = old_node.text.split(delimiter, 1)
            delim_index = old_node.text.find(delimiter)
            link_node = TextNode(md_links[0][0], TextType.LINK, md_links[0][1])
            for text_string in split_string:
                if text_string != "":
                    new_nodes.append(TextNode(text_string, TextType.TEXT))
            if delim_index == 0:
                new_nodes.insert(0, link_node)
            # i.e. the delimiter is at the end of the string
            elif delim_index == len(old_node.text) - (len(delimiter)):
                new_nodes.append(link_node)
            # The link must be between two text nodes
            else:
                new_nodes.insert(1, link_node)

        else:
            delimiters = []
            for tup in md_links:
                delim = f"[{tup[0]}]({tup[1]})"
                delimiters.append(delim)
            text_strings = []
            node_string = old_node.text
            for i in range(len(md_links)):
                link = md_links[i]
                delim = f"[{link[0]}]({link[1]})"
                # split_string = re.split(r"(delim)", node_string)
                split_string = node_string.split(delim, 1)
                if len(split_string[0]) > 0:
                    # text_strings.append(split_string[0])
                    new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                # text_strings.append(delim)
                # new_nodes.append(TextNode(delim, TextType.TEXT))
                link_node = TextNode(link[0], TextType.LINK, link[1])
                new_nodes.append(link_node)
                node_string = split_string[1:][0]
            print(old_node.text)
            # print(text_strings)

    return new_nodes


main()
