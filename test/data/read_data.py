import unittest
from data.read_data import ReadJson

class TestReadJson(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """테스트를 실행할 때 단 1번 실행 됩니다."""
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        """테스트를 끝낼 때 단 1번 실행 됩니다."""
        print('teardownClass')

    def setUp(self):
        """각각의 테스트 메소드가 실행될 때 실행 됩니다."""
        print('setUp')

    def tearDown(self):
        """각각의 테스트 메소드가 끝날 때 실행 됩니다."""
        print('tearDown')

    def test_init(self):
        """ 생성 테스트 """
        r = ReadJson()
        a1 = r.get_data_class_processes()
        a2 = r.get_data_class_processes()
        print(id(a1))
        print(id(a2))
        print(a1)

    def test_get_dataframe(self):
        """ 데이터 프레임 확인하기 """
        r = ReadJson()
        a1 = r.get_dataframe()
        print(a1)
