from textnode import TextNode, TextType


def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    # italic_node = TextNode("This is text with an _italic word_ in it", TextType.TEXT)
    bold_node = TextNode("This is text with a **bold word** word", TextType.TEXT)
    # bad_node = TextNode("This is text `with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
    # new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    # new_nodes = split_nodes_delimiter([italic_node], "_", TextType.ITALIC)
    print(new_nodes)
    should_be = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    # print(should_be)
    # print(TextType.CODE)


# It takes a list of "old nodes", a delimiter, and a text type.
# It should return a new list of nodes, where any "text" type
# nodes in the input list are (potentially) split into multiple
# nodes based on the syntax. For example, given the following input:
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


main()
