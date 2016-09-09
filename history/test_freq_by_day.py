import unittest

class TestFun(unittest.TestCase):
    def setUp(self):
        print 'do before class...'
    def tearDown(self):
        print 'do after class...'
    def test_extract_data(self):
        print 'test extract_data...'
        self.assertEqual(1,extract_data(13392019202)[0])
    def test_avg(self):
        print 'test avg...'
        self.assertEqual(1,avg(13392019202))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFun)
    unittest.TextTestRunner(verbosity =2).run(suite)
