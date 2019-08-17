import unittest

import test_ping_test
import test_http_test
import test_https_test
import test_dns_test
import test_tcp_test


def suite():
    alltests = unittest.TestSuite()
    alltests.addTest(test_ping_test.PingTest())
    alltests.addTest(test_http_test.http_suite)
    alltests.addTest(test_https_test.https_suite)
    alltests.addTest(test_dns_test.DNSTest())
    alltests.addTest(test_tcp_test.TCPTest())
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')