# Static Site Notes

I wrote a function for the split nodes delimiter, but this wasn't correct. I
assumed only one pair of delimiters per node, but you should check for multiple.

The course solution uses a nested loop, so for each node in old nodes, split the
line based on a delimiter. If the length of the array produced is not equal, the
markdown is not valid. Now start an inner loop using a range. If i is odd, you
know the new node should be of a given type.

## Regexes

The regex below matches the first part of :

```
This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)
(\!\[[\w\s]+\])
```

So this gives us the 'alt' element of the string.
https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)

(\!\[[\w\s]+\]\(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\))

## More Regexes

```python
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
```

For the image markdown, just look for '!' first, then '\['. Now you need round
brackets for the first group, the alt text. So you want whatever is inside the
square brakets. This looks like '(^\[\]_)'. The caret symbol negates what
follows, so grab anything that isn't a square bracket. The asterisk looks for 0
or more characters of this type. Just use the same pattern again for the round
brackets, e.g. '(^\(\)'

```
([^\[\]]_)
([^\(\)]*)
```

The link markdown is the same, except it has `(?<!!)`, which checks that there
isn't a '!' before the opening square bracket, i.e. we don't want to match on
images

## Image and Link Node function

If there are no image links in the node's text, just append it to your
'new_nodes' list. Otherwise create your 'split_nodes' list, and create the new
image node.

```
"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
```

If there's only one delimiter, i.e. if the list of tuples is length 1, just
split using the alt and url text, and the resulting array will have the plain
text only.

With more than one delimiter, use the first delimiter to get the 0th element.

Now I can get the text nodes from each string using split.

### Re-creating the split string

Once I have split the string using the link delimiter, I'm left with a problem.
How do you put the nodes back together in the right order?

I have a solution for the case where there is one link in the string. When there
are multiple delimiters, I split the string with each one, and extract the text
string, which is always the 0th element in the split string.

## Solution for image / link extraction

My fix was to grab the text from the old node, having extracted the image data,
and then create the delimiter based on this, i.e. wrap the alt text in ![] etc.
If you split the string using this delimiter, and '1' you should get a two
length array. The 0th element will be a normal text string, which could be an
empty string '', so check for this. The image node will be the 'ith' element in
your list of image tuples, so just create the node and append it. You now have
to remember to update the node string to exclude what you just added, so
everything from 1 to the end of the array.

```python
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
        for i in range(len(md_links)):
            link = md_links[i]
            delim = f"[{link[0]}]({link[1]})"
            split_string = node_string.split(delim, 1)
            if len(split_string) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if len(split_string[0]) > 0:
                new_nodes.append(TextNode(split_string[0], TextType.TEXT))
            link_node = TextNode(link[0], TextType.LINK, link[1])
            new_nodes.append(link_node)
            node_string = split_string[1:][0]
        if len(node_string) > 0:
            new_nodes.append(TextNode(node_string, TextType.TEXT))
    return new_nodes
```

There's no reason for the 'for i in range' loop, so this is just a 'for in'
loop now. The second if check in the loop checks the length of the first string.
This makes sense, but you can just check for an empty string here, which is more
clear. The assignment to node_string is too complicated. This value will be just
the 2nd element, or 1th index in the split string array, which we now know must
have 2 elements, so just grab this, there's no need for list slicing here.

### Course solution

The course solution ditches the count index, and uses a simple for loop.

```python
def split_nodes_link_course(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

```

## MD to HTML

Given some markdown like this:

```python
md_short = """
    This is **bolded** paragraph
    text in a p
    tag here

    """
```

Create the right parent node, e.g. a 'p' node in this case.

```python
should_be = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>div>"
```

```python
super().__init__(tag, None, children, props)
```

For the paragraph example, you create a parent node with a 'p' tag. The parent
node has no value, do not try to create a html string for it. The 'p' tag has
child nodes, these are leaf nodes. Some are normal text, some are bold, italic,
or underlined. For example:

```python
node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

node.to_html()
```

becomes:

```html
<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>
```

## Recursive file copying

I loop over the contents of the src directory.
