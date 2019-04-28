import unittest

import helpers

from ScoringEngine.engine import helper


class PingTest(unittest.TestCase):
    def runTest(self):
        m = __import__('PING')
        m.test(None, {'ip': '8.8.8.8'})
        status, info = helper.get_status()
        print(info)
        assert status == True


if __name__ == "__main__":
    unittest.main()