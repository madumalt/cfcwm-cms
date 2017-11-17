import logging
import logging.config
import os
import json
from datetime import datetime, timedelta
from os.path import join as pjoin

import unittest2 as unittest
from cms_utils.InterpolationStrategy import InterpolationStrategy


class UtilInterpolationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_dir = os.path.dirname(os.path.realpath(__file__))
        # config = json.loads(open(pjoin(cls.root_dir, '../../observation/config/CONFIG.json')).read())

        # Initialize Logger
        logging_config = json.loads(open(pjoin(cls.root_dir, '../../observation/config/LOGGING_CONFIG.json')).read())
        logging.config.dictConfig(logging_config)
        cls.logger = logging.getLogger('UtilInterpolationTest')
        cls.logger.addHandler(logging.StreamHandler())
        cls.logger.info('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        self.logger.info('setUp')

    def tearDown(self):
        self.logger.info('tearDown')

    def test_average_larger(self):
        time_interval = timedelta(seconds=60)
        timeseries = [
            [datetime.strptime('2017-11-16 13:50:00', '%Y-%m-%d %H:%M:%S'), 4.0],
            [datetime.strptime('2017-11-16 13:55:00', '%Y-%m-%d %H:%M:%S'), 5.0],
            [datetime.strptime('2017-11-16 14:01:00', '%Y-%m-%d %H:%M:%S'), 6.0]
        ]
        new_timeseries = \
            InterpolationStrategy.get_strategy_for_larger(InterpolationStrategy.Average)(timeseries, time_interval)
        self.assertEqual(len(new_timeseries), 11)

    def test_average_smaller(self):
        time_interval = timedelta(seconds=60)
        # NOTE: Assume that there isn't any gaps in the timeseries
        # Gaps need to be fulfill before going to feed into the function
        timeseries = [
            [datetime.strptime('2017-11-15 08:20:29', '%Y-%m-%d %H:%M:%S'), 1.0],
            [datetime.strptime('2017-11-15 08:20:45', '%Y-%m-%d %H:%M:%S'), 2.0],
            [datetime.strptime('2017-11-15 08:21:01', '%Y-%m-%d %H:%M:%S'), 3.0],
            [datetime.strptime('2017-11-15 08:21:17', '%Y-%m-%d %H:%M:%S'), 4.0],
            [datetime.strptime('2017-11-15 08:21:33', '%Y-%m-%d %H:%M:%S'), 5.0],
            [datetime.strptime('2017-11-15 08:21:49', '%Y-%m-%d %H:%M:%S'), 6.0],
            [datetime.strptime('2017-11-15 08:22:05', '%Y-%m-%d %H:%M:%S'), 7.0],
            [datetime.strptime('2017-11-15 08:22:21', '%Y-%m-%d %H:%M:%S'), 8.0],
            [datetime.strptime('2017-11-15 08:22:37', '%Y-%m-%d %H:%M:%S'), 9.0],
            [datetime.strptime('2017-11-15 08:22:53', '%Y-%m-%d %H:%M:%S'), 10.0],
            # No cases like below
            # [datetime.strptime('2017-11-16 12:46:03', '%Y-%m-%d %H:%M:%S'), 1.0],
            # [datetime.strptime('2017-11-16 12:46:19', '%Y-%m-%d %H:%M:%S'), 1.0],
            # [datetime.strptime('2017-11-16 12:46:35', '%Y-%m-%d %H:%M:%S'), 1.0],
            # [datetime.strptime('2017-11-16 12:46:51', '%Y-%m-%d %H:%M:%S'), 1.0],
            # [datetime.strptime('2017-11-16 12:47:07', '%Y-%m-%d %H:%M:%S'), 1.0]
        ]
        new_timeseries = \
            InterpolationStrategy.get_strategy_for_smaller(InterpolationStrategy.Average)(timeseries, time_interval)
        print(new_timeseries)
        self.assertEqual(len(new_timeseries), 3)
