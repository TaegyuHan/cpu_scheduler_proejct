import json
import os
from copy import deepcopy
import pandas as pd

from data.process import (
    Time, Count, Process
)


class ReadJson:
    """
        json 데이터 읽기 클래스

        프로세스 데이터의 json파일을 읽어 인스턴스를 생성합니다.
        폴더 경로 : ./json
    """

    DATA_FILE_NAME = "data.json"

    def __init__(self):
        # json 데이터 읽는 부분
        with open((f'{os.path.dirname(__file__)}'
                   f'/json/{self.DATA_FILE_NAME}')) as json_file:
            self._data = json.load(json_file)

        # 프로레스 수
        self._processes_count = self._data["processesCount"]

        # 0인 경우
        if self._processes_count == Count.ZERO:
            raise Exception(f"프로세스 수가 {self._processes_count}입니다. 프로세스를 넣어주세요")
        # 음수인 경우
        elif self._processes_count < Count.ZERO:
            raise Exception(f"프로세스 수가 {self._processes_count}입니다. 양수 값으로 넣어주세요")

        # 프로세스 디테일
        self._processes = self._data["data"]

        # 프로세스 디테일 개수 확인
        if not self._processes:
            raise Exception("json 데이터에 프로세스가 존재하지 않습니다.")

        # 프로세스 디테일 수 확인
        elif self._processes_count != len(self._processes):
            raise Exception("json 파일의 processesCount와 data의 프로세스 수가 같지 않습니다.")

        self._check_process_data()

        self._init_make_process_data_class()

    def _check_process_data(self):
        """ 프로세스 데이터 확인하기

            프로그램에 부적절한 데이터가 들어오는 것을 확인합니다.
        """

        # 동일한 id 확인하기
        id_same_check = set()
        arrival_same_check = set()

        for proces in self._processes:
            id_same_check.add(proces["id"])
            arrival_same_check.add(proces["arrivalTime"])

            if proces["arrivalTime"] < Time.ZERO:
                raise Exception("arrivalTime 음수에 도착할 수 없습니다. 0이상의 정수로 입력해주세요.")

            elif proces["serviceTime"] < Time.ZERO:
                raise Exception("serviceTime 음수를 가질 수 없습니다. 1이상의 양의 정수로 입력해주세요.")

            elif proces["priority"] < 0:
                raise Exception("priority는 양의 정수로 입력해주세요.")

            elif proces["timeSlice"] <= Time.ZERO:
                raise Exception("timeSlice는 1이상의 양의 정수로 입력해주세요.")

        if len(id_same_check) != self._processes_count:
            raise Exception("모든 프로세스 id가 달라야 합니다.")

        elif len(arrival_same_check) != self._processes_count:
            raise Exception("동일한 시간에 도착하는 프로세스는 없어야 합니다.")

    def _init_make_process_data_class(self):
        """ 프로세스 데이터 클래스 생성하기 """
        self._data_class_processes = []
        for process in self._processes:
            self._data_class_processes.append(
                Process(
                id=process["id"],
                arrival_time=process["arrivalTime"],
                service_time=process["serviceTime"],
                cpu_run_time=Time.ZERO,
                priority=process["priority"],
                time_slice=process["timeSlice"],
                stop_time=process["arrivalTime"]))

        # 도착한 순으로 정렬
        self._data_class_processes.sort(key=lambda x: x.arrival_time,
                                        reverse=True)

    def get_data_class_processes(self):
        """ 데이터 프로세스 클래스 얻기 """
        return deepcopy(self._data_class_processes)

    def get_pandas_dataframe(self):
        """ 판다스 데이터 프레임 생성 """
        tmp_data = {
            "id": [],
            "arrivalTime": [],
            "serviceTime": [],
            "priority": [],
            "timeSlice": [],
        }
        for row in self._processes:
            for key, value in row.items():
                tmp_data[key].append(value)

        return pd.DataFrame.from_dict(tmp_data)

read_json = ReadJson()