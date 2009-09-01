processors = {}

def register(cls, extensions):
    for ext in extensions:
        processors[ext] = cls

class MarkupProcessor(object):
    """
    Accepts a block of text as it's input, and applies "render" to it
    """
    extensions = []
    description = "Applies no methods to the content"

    def __init__(self, content):
        assert self.extensions
        assert self.description
        self.content = content

    def process(self):
        return self.content

class NullProcessor(MarkupProcessor):
    extensions = [".txt", ""]
    description = "Does nothing to the text"

    def process(self):
        return self.content
register(NullProcessor, NullProcessor.extensions)

class MarkdownProcessor(MarkupProcessor):
    """
    inserts paragraphs where there were double spaces
    """
    extensions = [".markdown", ".md", ".mdown", ".mkd", ".mkdn"]
    description = "inserts paragraphs where there were double spaces"

    def process(self):
        import markdown
        return markdown.markdown(self.content) 
register(MarkdownProcessor, MarkdownProcessor.extensions)

class TextileProcessor(MarkupProcessor):
    extensions = [".textile"]

    def process(self):
        import textile
        return textile.textile(self.content)
register(TextileProcessor, TextileProcessor.extensions)

def markup(extension):
    if extension in processors:
        processor = processors[extension]
    else:
        processor = processors[".txt"]

    def process(content):
        return processor(content).process()

    return process

def extensions():
    return processors.iterkeys()
