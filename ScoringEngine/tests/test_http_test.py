import unittest

import helpers

from ScoringEngine.engine import helper

class HTTPTest(unittest.TestCase):
    def testBasic(self):
        m = __import__('HTTP')
        m.test(None, {'ip': '93.184.216.34', 'port': 80, 'team_server_id':1, 'service_id':1})
        status, info = helper.get_status()
        assert status == True

    def testAdvanced(self):
        m = __import__('HTTP')
        m.test(None, {'ip': '93.184.216.34', 'port': 80, 'team_server_id': 2, 'service_id': 1})
        status, info = helper.get_status()
        assert status == True


http_suite = unittest.TestSuite()
http_suite.addTest(HTTPTest('testBasic'))
http_suite.addTest(HTTPTest('testAdvanced'))


if __name__ == "__main__":
    unittest.main()