class FeedFormatter(object):
    def __init__(self):
        pass

    def format(self, contents):
        # To be overwritten by derived classes
        pass


class PPrintFormatter(FeedFormatter):
    def __init__(self):
        super(PPrintFormatter, self).__init__()

    def format(self, contents):
        result = ''
        for content in contents:
            for key, value in content.items():
                result += u'{}: {}\n'.format(key, value)
            result += u'\n'  # A line padding between the entries
        return result


class ListFormatter(FeedFormatter):
    def __init__(self):
        super(ListFormatter, self).__init__()

    def format(self, contents):
        result = ''
        for content in contents:
            for value in content.values():
                result += u'{}\n'.format(value)
        return result
