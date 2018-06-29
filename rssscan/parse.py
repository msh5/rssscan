from collections import OrderedDict
import os

import feedparser


class FeedParser(object):
    def __init__(self, target):
        self.target = target

    def parse(self):
        # To be overwritten by derived classes
        pass

    def parse_feed(self, url_or_filepath):
        feed = feedparser.parse(url_or_filepath)
        result = []
        for entry in feed.entries:
            items = [('title', entry.title), ('description', entry.summary),
                     ('pubDate', entry.published)]
            result.append(OrderedDict(items))
        return result


class FileParser(FeedParser):
    def __init__(self, filepath):
        super(FileParser, self).__init__(filepath)

    def parse(self):
        filepath = self.target
        if not os.path.exists(filepath):
            return None
        # Buffer file contents once to work-around for encoding error
        buffer = ""
        with open(filepath) as fp:
            buffer = fp.read()
        return self.parse_feed(buffer)


class HTTPParser(FeedParser):
    def __init__(self, url):
        super(HTTPParser, self).__init__(url)

    def parse(self):
        url = self.target
        return self.parse_feed(url)
