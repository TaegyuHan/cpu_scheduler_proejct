from dataclasses import dataclass


class HRN:
    """ HRN value """
    ZERO = 0


class Time:
    """ 프로세스 시간 """
    ZERO = 0


class Count:
    """ 프로세스 개수 """
    ZERO = 0


@dataclass
class Process:
    """ 프로세스 데이터 클래스 """
    id: int # 프로세스 아이디
    arrival_time: int # 프로세스 도착 시각
    service_time: int # 프로세스 동작 시간
    cpu_run_time: int # cpu에 돌아간 시간
    priority: int # 프로세스 우선순위
    time_slice: int # 프로세스 슬라이스 시간
    stop_time: int # 프로세스 멈춘 시간

    def __lt__(self, other):
        return self.remain_service_time < other.remain_service_time

    @property
    def remain_service_time(self):
        """ 서비스 남은 시간 """
        return self.service_time - self.cpu_run_time

    @property
    def check_time_out(self):
        """ 시간초과 확인하기 """
        try:
            return self.cpu_run_time % self.time_slice
        except ZeroDivisionError:
            return 0

    @property
    def rr_cpu_service_time(self):
        """ rr cpu 동작시간 """
        if self.remain_service_time >= self.time_slice:
            return self.time_slice
        return self.remain_service_time

    def get_hrn(self, time):
        """ hrn 값 얻기 """
        try:
            return (time - self.arrival_time + self.service_time) / self.service_time
        except ZeroDivisionError:
            return HRN.ZERO