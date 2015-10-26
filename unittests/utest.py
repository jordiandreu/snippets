import logging
import sys
from unittest import TestCase, TestSuite, TextTestRunner


class TestCaseValue(TestCase):
    def __init__(self, value=0):
        super(TestCaseValue, self).__init__()
        # mandatory if you want to add logging
        self.logger = logging.getLogger("TestCaseValue")
        self.value = value

    def setUp(self):
        self.logger.debug('Setting Up...')

    def runTest(self):
        self.logger.debug('Running Test...')
        msg_e = 'Input value different from 0'
        self.assertEqual(self.value, 0, msg_e)
        msg_g = 'Input value smaller than -1'
        self.assertGreater(self.value, -1, msg_g)
        msg_l = 'Input value greater than 10'
        self.assertLess(self.value, 10, msg_l)
        msg = 'Running with value = %s' % self.value
        self.logger.info(msg)

    def tearDown(self):
        self.logger.debug('Cleaning...')


class TestCaseString(TestCase):
    def __init__(self, value=None):
        super(TestCaseString, self).__init__()
        # mandatory if you want to add logging
        self.logger = logging.getLogger("TestCaseString")
        self.value = value

    def setUp(self):
        self.logger.debug('Setting Up...')

    def runTest(self):
        self.logger.debug('Running Test...')
        msg_e = 'Input value different from None'
        self.assertEqual(self.value, None, msg_e)
        msg = 'Running test with string = %s' % self.value
        self.logger.info(msg)

    def tearDown(self):
        '''
        TearDown is only executed if setUp was executed with success.
        :return:
        '''
        self.logger.debug('Cleaning...')


class UTestSuite(TestSuite):
    pass


def utest():

    logger = logging.getLogger("TestSuite")

    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestSuite").setLevel(logging.INFO)
    logging.getLogger("TestCaseString").setLevel(logging.DEBUG)
    logging.getLogger("TestCaseValue").setLevel(logging.INFO)

    suite = TestSuite()
    case_value_error = TestCaseValue(1)
    #case_value_passed = TestCaseValue()
    suite.addTest(case_value_error)
    #suite.addTest(case_value_passed)

    case_string_error = TestCaseString('Hola')
    #case_string_passed = TestCaseString()
    suite.addTest(case_string_error)
    #suite.addTest(case_string_passed)

    result = TextTestRunner(verbosity=0).run(suite)
    logger.info('Errors: %s' % len(result.errors))
    logger.info('Failures: %s' % len(result.failures))

if __name__ == '__main__':

    utest()
