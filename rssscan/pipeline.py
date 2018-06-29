DEFAULT_PARAMS = {}


class ScanPipeline(object):
    def __init__(self):
        self.parsers = []
        self.filters = []
        self.formatter = None
        self.emitter = None

    def add_parser(self, instance):
        self.parsers.append(instance)

    def add_filter(self, instance):
        self.filters.append(instance)

    def set_formatter(self, instance):
        self.formatter = instance

    def set_emitter(self, instance):
        self.emitter = instance

    def run(self):
        contents = None
        for parser in self.parsers:
            contents = parser.parse()
            if contents is not None:
                break
        assert contents is not None

        for filter_ in self.filters:
            contents = filter_.filter(contents)

        body = self.formatter.format(contents)
        self.emitter.emit(body)