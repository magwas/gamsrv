#!/usr/bin/python

import unittest

from lib import log

class TestLog(unittest.TestCase):

	def test_proto(self):
		log.log(log.LOG_DEBUG,"test","tester","logger",a=1, b=2, c="three")

if __name__ == '__main__':
	unittest.main()

