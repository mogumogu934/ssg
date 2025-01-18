class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        
        strings = []
        for prop in self.props:
            stripped_key = prop.strip('"')
            string = f'{stripped_key}="{self.props[prop]}"'
            strings.append(string)
        return " " + " ".join(strings)

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"
