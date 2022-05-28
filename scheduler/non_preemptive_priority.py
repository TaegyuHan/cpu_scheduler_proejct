import pandas as pd
import heapq
from data.process import Time
import scheduler


class NPS(scheduler.AbstractSchedule):
    """
        비선점 스케쥴링(Nonpreemptive Scheduling) 스케줄링

        Nonpreemptive Scheduling (NPS)
        비선점 스케쥴링(Non-preemptive Scheduling)은 프로세스가
        자원을 할당받았을 경우 자원을 스스로 반납할 때까지 계속 그
        자원을 사용하도록 허용하는 정책이다.
    """

    NAME = "Nonpreemptive Scheduling (NPS)"

    def __init__(self):
        super().__init__()
        self._ready_queue = []
        self._run()

    def _update_ready(self):
        """ 준비 상태 최신화 """
        # 프로세스 없으면 실행 안함
        if not self._creation: return

        process = self._creation.pop()

        # 도착 시간이 안지난 경우
        if process.arrival_time > self.time:
            self.arrival_times.append(self.time)
            self._creation.append(process)
            return

        heapq.heappush(self._ready_queue,
                       (process.priority, process))

    def _cpu_empty_check(self):
        """ cpu 장치 """
        # cpu에 프로세스 실행중
        if len(self._cpu) == scheduler.CPU_FULL:
            return False
        # cpu 실행 안할 때
        return True

    def _cpu_work(self):
        """ cpu 프로세스 동작하기 """
        # CPU에 프로세스가 없으면 PASS
        if not self._cpu: return

        process = self._cpu.pop()
        process.cpu_run_time += 1

        if process.remain_service_time == Time.ZERO:
            self._end_process.append(process)
            self.end_times.append(self.time)
        else:
            self._cpu.append(process)

    def _dispatch(self):
        """ 디스 패치 프로세스 준비상태에서 실행상태로 변경 """

        # 준비 큐에 데이터 없으면 PASS
        if not self._ready_queue: return
        _, process = heapq.heappop(self._ready_queue)
        wait_time = self.time - process.stop_time

        # 프로세스가 기다린 시간 넣기
        if wait_time > Time.ZERO:
            self._data_frame_list.append(
                [
                    "wait",
                    f"P{process.id}",
                    process.stop_time,
                    self.time,
                    wait_time
                ]
            )

        self._cpu.append(process)

        service_end_time = self.time + process.service_time
        # 프로세스가 동작한 시간 넣기
        self._data_frame_list.append(
            [
                "run",
                f"P{process.id}",
                self.time,
                service_end_time,
                process.service_time
            ]
        )

    def _time_out(self):
        """ 시간 초과 """
        # NPS 시간초과 없음

    def _break_check(self):
        """ 프로세스 실행 전부 완료했는지 확인하기 """
        if len(self._end_process) == self._process_count:
            return False
        return True

    def _run(self):
        """ 실행상태 """
        self.time = 0
        while self._break_check():
            self._update_ready()

            if self._cpu_empty_check():
                self._dispatch()

            self._cpu_work()
            self.time += 1

    def get_pandas_data_frame(self):
        """ 판다스 데이터 프레임 얻기 """
        data_frame = pd.DataFrame(self._data_frame_list,
                     columns=self.PANDAS_COL_NAMES)

        return data_frame