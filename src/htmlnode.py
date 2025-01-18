class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        
        strings = []
        for prop in self.props:
            stripped_key = prop.strip('"')
            string = f'{stripped_key}="{self.props[prop]}"'
            strings.append(string)
        return " " + " ".join(strings)

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if not self.value:
            raise ValueError
        
        if self.tag is None:
            return self.value

        html_props = ""
        if self.props is not None:
            strings = []
            for prop in self.props:
                string = f'{prop}="{self.props[prop]}"'
                strings.append(string)
            html_props = " ".join(strings)
        return f'<{self.tag}{" " + html_props if html_props else ""}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is None")
        
        if not self.children:
            raise ValueError("missing value for children")
        
        strings = []
        for child in self.children:
            child_html = child.to_html()
            strings.append(child_html)
        return f'<{self.tag}>{"".join(strings)}</{self.tag}>'
