# coding=utf-8
import abc, six
from datetime import datetime


class TItem:
    def __init__(self, timestamp, content):
        self.timestamp = timestamp
        self.content = content
    def __str__(self):
        return "%s|%s" % (self.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z"),
           self.content)

class Timeline:
    def __init__(self, name = None):
        self.itemSet = set()
        self.name = name
    def add(self, item):
        if item.timestamp:
            self.itemSet.add(item)
        else:
            raise AttributeError("No valid timestamp found!")
    def getList(self):
        if not bool(self.itemSet):
            return None
        return sorted(list(self.itemSet), key=lambda x:x.timestamp)
    def __repr__(self):
        if not bool(self.itemSet):
            return "Timeline is still empty."
        l = self.getList()
        pre = ("Timeline: %s\n" % self.name ) if self.name else ""
        return pre + "\n".join(map(str,l))
