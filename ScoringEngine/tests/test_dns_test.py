import unittest

import helpers

from ScoringEngine.engine import helper, set_helper

class DNSTest(unittest.TestCase):
    def runTest(self):
        m = __import__('DNS')
        m.test(None, {'ip': '8.8.8.8', 'port': 53, 'team_server_id': 3, 'service_id': 1})
        status, info = helper.get_status()
        assert status == True


if __name__ == "__main__":
    unittest.main()