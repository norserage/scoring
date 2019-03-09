import unittest

import helpers

from ScoringEngine.engine import helper, set_helper

class HTTPHelper(helpers.MockEngineHelperBase):
    def get_service_config_old(self, team_server_id, service_id):
        return {
            'url': '/test',
            'regex': '404'
        }

class HTTPSTest(unittest.TestCase):
    def testBasic(self):
        m = __import__('HTTPS')
        m.test(None, {'ip': '93.184.216.34', 'port': 443, 'team_server_id':1, 'service_id':1})
        status, info = helper.get_status()
        assert status == True

    def testAdvanced(self):
        m = __import__('HTTPS')
        m.test(None, {'ip': '93.184.216.34', 'port': 443, 'team_server_id': 2, 'service_id': 1})
        status, info = helper.get_status()
        assert status == True


https_suite = unittest.TestSuite()
https_suite.addTest(HTTPSTest('testBasic'))
https_suite.addTest(HTTPSTest('testAdvanced'))


if __name__ == "__main__":
    unittest.main()