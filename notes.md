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
