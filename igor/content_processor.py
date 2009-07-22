class ContentProcessor(object):
    """
    Accepts a block of text as it's input, and applies "render" to it
    """
    def __init__(self, content):
        self.content = content

    def render(self):
        self.content

class BasicProccessor(ContentProcessor):
    """
    inserts paragraphs where there were double spaces
    """
    def render(self):
        parts = self.content.split("\n\n")
        return "<p>" + "</p><p>".join(parts) + "</p>"
    
