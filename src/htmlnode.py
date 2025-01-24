class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

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
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if not self.value and self.tag not in ["img", "br", "hr", "input"]:  # it's valid for these tags to have no value
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
            
        if self.tag in ["img", "br", "hr", "input"]:
            return f'<{self.tag}{" " + html_props if html_props else ""} />'

        return f'<{self.tag}{" " + html_props if html_props else ""}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        self.children = children or []
        
    def to_html(self):
        if not self.tag:
            raise ValueError("A ParentNode must have a valid tag!")

        html_children = []
        for child in self.children:
            if child and hasattr(child, 'to_html') and callable(child.to_html):
                html_children.append(child.to_html())
            else:
                raise ValueError(f"Invalid child found: {child}")

        children_html = ''.join(html_children)
        return f'<{self.tag}>{children_html}</{self.tag}>'
