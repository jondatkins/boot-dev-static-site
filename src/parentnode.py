from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        parent_opening_tag = f"<{self.tag}{self.props_to_html()}>"
        parent_closing_tag = f"</{self.tag}>"
        child_html = ""
        for child in self.children:
            child_html += child.to_html()

        parent_tag = f"{parent_opening_tag}{child_html}{parent_closing_tag}"
        return parent_tag

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children})"
