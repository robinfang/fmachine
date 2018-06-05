# coding=utf-8
import unittest
import time
from timeline import *
from datetime import datetime

class TestTimeline(unittest.TestCase):
    def test_timeline(self):
        t = Timeline("a")
        self.assertIsNone(t.getList())
        i = TItem(datetime.now(),"1,i")
        time.sleep(2)
        j = TItem(datetime.now(),"2,j")
        t.add(j)
        t.add(i)
        # t.add(TItem("","3333"))
        print t
