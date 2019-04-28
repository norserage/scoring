import unittest

import helpers

from ScoringEngine.engine import helper


class TCPTest(unittest.TestCase):
    def runTest(self):
        m = __import__('TCP')
        m.test(None, {'ip': '93.184.216.34', 'port': 80})
        status, info = helper.get_status()
        print(info)
        assert status == True


if __name__ == "__main__":
    unittest.main()