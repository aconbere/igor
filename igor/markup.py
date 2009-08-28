processors = {}

class MarkupProcessor(object):
    """
    Accepts a block of text as it's input, and applies "render" to it
    """
    extensions = []
    description = "Applies no methods to the content"

    def __init__(self):
        assert self.extensions
        assert self.description

        for extension in self.extensions:
            processors[extension] = self


    def process(self, content):
        return content

class NullProcessor(MarkupProcessor):
    extensions = [".txt", ""]
    description = "Does nothing to the text"

    def process(self, content):
        return content
NullProcessor()

class MarkdownProcessor(MarkupProcessor):
    """
    inserts paragraphs where there were double spaces
    """
    extensions = [".markdown", ".md", ".mdown", ".mkd", ".mkdn"]
    description = "inserts paragraphs where there were double spaces"

    def process(self, content):
        import markdown
        return markdown.markdown(content) 
MarkdownProcessor()

class TextileProcessor(MarkupProcessor):
    extensions = [".textile"]

    def process(self, content):
        import textile
        return textile.textile(content)
TextileProcessor()

def markup(extension):
    if extension in processors:
        processor = processors[extension]
    else:
        processor = processors[".txt"]

    def process(content):
        return processor.process(content)

    return process

def extensions():
    return processors.iterkeys()
