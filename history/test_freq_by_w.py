import unittest
import os
import sys
from freq_by_you import by_day
import csv


class Test_fby(unittest.TestCase):
    def setUp(self):
        print 'ready .....'
    def tearDown(self):
        print 'DONE'
    def test_by_day(self):
        print '---test begin---'
        temp_d = by_day().handle()
        tn = '18861823294.week.csv'
        reader = csv.reader(file(tn,'rb'))
        tp = []
        for line in reader:
            tp.append(line[1])
        self.assertEquals(tp[2],'1.0')
        print '------end--------'


if __name__ == "__main__":
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_fby)
        unittest.TextTestRunner(verbosity =2).run(suite)
