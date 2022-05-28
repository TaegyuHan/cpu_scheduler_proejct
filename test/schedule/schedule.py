import unittest
from scheduler.first_come_first_served import FCFS
from scheduler.shortest_job_next import SJF
from scheduler.highest_response_ratio_next import HRN
from scheduler.round_robin import RR
from scheduler.shortest_remaining_time import SRT
from scheduler.non_preemptive_priority import NPS
from scheduler.preemptive_priority import PS


class TestFCFS(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = FCFS()
        print(f.get_pandas_data_frame())


class TestSJF(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = SJF()
        print(f.get_pandas_data_frame())


class TestHRN(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = HRN()
        print(f.get_pandas_data_frame())


class TestRR(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = RR()
        print(f.get_pandas_data_frame())


class TestSRT(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = SRT()
        print(f.get_pandas_data_frame())


class TestNPP(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = NPS()
        print(f.get_pandas_data_frame())


class TestPS(unittest.TestCase):

    def test_init(self):
        """ 생성 테스트 """
        f = PS()
        print(f.get_pandas_data_frame())