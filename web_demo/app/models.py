# coding=utf-8
import abc
import six
from datetime import datetime
import sqlite3
import pdb

dbfile = "fmachine_demo.db"


class TimelineStore:

    def __init__(self, dbfile = dbfile):
        self.dbfile = dbfile
        self.conn = sqlite3.connect(self.dbfile, detect_types=sqlite3.PARSE_DECLTYPES)

    def getAllTItem(self):
        cur = self.conn.cursor()
        cur.execute("select * from titem order by timestamp ASC")
        result = Timeline()
        for row in cur:
            result.add(TItem(row[0], row[1], row[2]))
        cur.close()
        return result

    def getTItem(self, tItem):
        cur = self.conn.cursor()
        cur.execute("select * from titem where timestamp=? and title=?", (tItem.timestamp, tItem.title) )
        # print (tItem.timestamp, tItem.title)
        row = cur.fetchone()
        # pdb.set_trace()
        tItem = TItem(row[0], row[1], row[2])
        return tItem

    def saveTItem(self, tItem):
        cur = self.conn.cursor()
        try:
            cur.execute("insert into titem values(?,?,?)", (tItem.timestamp, tItem.title, tItem.content if  tItem.content else ""))
            self.conn.commit()
            cur.close()
            return tItem, True
        except sqlite3.IntegrityError as e:
            cur.execute("select * from titem where timestamp=? and title=?", (tItem.timestamp, tItem.title) )
            row = cur.fetchone()
            tItem = TItem(row[0], row[1], row[2])
            return tItem, False

    def deleteTItem(self,tItem):
        cur = self.conn.cursor()
        cur.execute("delete from titem where timestamp=? and title=?", (tItem.timestamp, tItem.title))
        self.conn.commit()
        cur.close()
        return True

    def close(self):
        self.conn.close()


class TItem:

    def __init__(self, timestamp, title, content = None):
        self.timestamp = timestamp
        self.title = title
        self.content = content
    def __str__(self):
        return "%s | %s | %s" % (self.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z"), self.title, self.content if self.content else "")


class Timeline:

    def __init__(self, name=None):
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
        return sorted(list(self.itemSet), key=lambda x: x.timestamp)

    def __repr__(self):
        if not bool(self.itemSet):
            return "Timeline is still empty."
        l = self.getList()
        pre = ("Timeline: %s\n" % self.name) if self.name else ""
        return pre + "\n".join(map(str, l))
