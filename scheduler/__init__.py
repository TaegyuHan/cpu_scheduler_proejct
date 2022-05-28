"""

    판다스 데이터 형식
      state process  start  finish  time
    0   run      P0      0      30    30
    1  wait      P1      3      30    27
    2   run      P1     30      48    18
    3  wait      P2      6      48    42
    4   run      P2     48      57     9
    5   run      P3     60      90    30
    6  wait      P0     70      90    20
    7   run      P0     90     100    10
"""
from collections import deque
from data.read_data import read_json
from abc import ABC, abstractmethod


class AbstractSchedule(ABC):
    """ 스케줄러 """

    STATE_RUN = "run"
    STATE_WAIT = "wait"
    PANDAS_COL_NAMES = ["state", "process", "start", "finish", "time"]

    def __init__(self):
        self._creation = read_json.get_data_class_processes()
        self._process_count = len(self._creation)
        self._ready_queue = deque([])
        self._end_process = []
        self._cpu = []
        self._data_frame_list = []

        # ploty line data
        self.arrival_times = []
        self.end_times = []

    @abstractmethod
    def _update_ready(self):
        """ 프로세스 준비 """

    @abstractmethod
    def _cpu_empty_check(self):
        """ CPU 빈것 확인하기 """

    @abstractmethod
    def _cpu_work(self):
        """ CPU 동작 """

    @abstractmethod
    def _dispatch(self):
        """ CPU로 프로세스 옮기기 """

    @abstractmethod
    def _time_out(self):
        """ 프로세스 시간 초과 """

    @abstractmethod
    def _break_check(self):
        """ 프로세스 실행 전부 완료했는지 확인하기 """

    @abstractmethod
    def _run(self):
        """ 스케줄러 실행 """

CPU_FULL = 1