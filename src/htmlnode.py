class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        html_attributes = ""
        for prop in self.props:
            html_attributes += f' {prop}="{self.props[prop]}"'
        return html_attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
