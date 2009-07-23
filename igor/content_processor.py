_processors = {}

class ContentProcessor(object):
    """
    Accepts a block of text as it's input, and applies "render" to it
    """
    extensions = []
    description = "Applies no methods to the content"

    def __init__(self):
        assert self.extensions
        assert self.description

        for extension in self.extensions:
            _processors[extension] = self


    def process(self, content):
        return content

class BasicProccessor(ContentProcessor):
    """
    inserts paragraphs where there were double spaces
    """
    extensions = [".txt", ""]
    description = "inserts paragraphs where there were double spaces"

    def process(self, content):
        parts = content.split("\n\n")
        return "<p>" + "</p><p>".join(parts) + "</p>"
BasicProccessor()

class MarkdownProcessor(ContentProcessor):
    """
    inserts paragraphs where there were double spaces
    """
    extensions = [".markdown", ".md", ".mdown", ".mkd", ".mkdn"]
    description = "inserts paragraphs where there were double spaces"

    def process(self, content):
        import markdown
        return markdown.markdown(content) 
MarkdownProcessor()

class TextileProccessor(ContentProcessor):
    extensions = [".textile"]

    def process(self, content):
        import textile
        return textile.textile(content)
MarkdownProcessor()

def process(content, extension=""):
    if extension in _processors:
        return _processors[extension].process(content)
    else:
        return _processors[".txt"].process(content)
