from collections import OrderedDict

import dateutil.parser


class RossoFilter(object):
    def __init__(self):
        pass

    def filter(self, contents):
        result = []
        for content in contents:
            items = []
            for key, value in content.items():
                if value is None:
                    items.append((key, None))
                else:
                    new_value = self.filter_each(key, value)
                    if new_value:
                        items.append((key, new_value))
            result.append(OrderedDict(items))
        return result

    def filter_each(self, key, value):
        # To be overwritten by derived classes
        pass


class ShortenFilter(RossoFilter):
    def __init__(self, attribute, maxlen):
        super(ShortenFilter, self).__init__()
        self.attribute = attribute
        self.maxlen = maxlen

    def filter_each(self, key, value):
        if key == self.attribute and len(value) > self.maxlen:
            value = value[:self.maxlen] + '...'
        return value


class ReplaceFilter(RossoFilter):
    def __init__(self, attribute, src_chars, dest_char):
        super(ReplaceFilter, self).__init__()
        self.attribute = attribute
        self.src_chars = src_chars
        self.dest_char = dest_char

    def filter_each(self, key, value):
        if key == self.attribute:
            for src_char in self.src_chars:
                value = value.replace(src_char, self.dest_char)
        return value


class TruncateFilter(ReplaceFilter):
    def __init__(self, attribute, src_chars):
        super(TruncateFilter, self).__init__(attribute, src_chars, '')


class DateToJpStyleFilter(RossoFilter):
    def __init__(self):
        super(DateToJpStyleFilter, self).__init__()

    def filter_each(self, key, value):
        if key == 'pubDate':
            pubdate_dt = dateutil.parser.parse(value)
            value = pubdate_dt.strftime('%Y-%m-%d(%a) %H:%M:%S')
        return value


class AttributeRemoveFilter(RossoFilter):
    def __init__(self, attr):
        super(AttributeRemoveFilter, self).__init__()
        self.attr = attr

    def filter_each(self, key, value):
        if key == self.attr:
            value = None
        return value
