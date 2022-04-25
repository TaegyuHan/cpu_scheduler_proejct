from dataclasses import dataclass

class Time:
    """ 프로세스 시간 """
    ZERO = 0

class Count:
    """ 프로세스 시간 """
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

    @property
    def remain_service_time(self):
        """ 서비스 남은 시간 """
        return self.service_time - self.cpu_run_time