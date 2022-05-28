import pandas as pd
from data.read_data import read_json
from view.timeline_plot import TimeGanttPlot


def get_pandas_statistics_table(model_key):
    """ 스케줄링 완료 판다스 데이터 통계화 하기 """
    process_df = read_json.get_pandas_dataframe()
    schedul_df = TimeGanttPlot.MODLE[model_key].get_pandas_data_frame()

    process_count = len(process_df)

    # 저장 딕셔너리 생성
    statistics_dict = {}
    for num in process_df.id.tolist():
        statistics_dict[f"P{num}"] = {}
    statistics_dict["average"] = {} # 평균

    # 대기 시간
    wait_time = schedul_df[schedul_df.state == "wait"].groupby(['process']).sum()["time"]
    for process_num in range(process_count):
        if (key := f"P{process_num}") in wait_time.index:
            statistics_dict[key]["wait_sum"] = wait_time.filter(like=f"P{process_num}", axis=0)
        else:
            statistics_dict[key]["wait_sum"] = 0
    statistics_dict["average"]["wait_sum"] = round(sum(wait_time)/process_count, 2)

    # 반환 시간
    tmp = []
    for num in process_df.id.tolist():
        arrival_time = int(process_df[process_df.id == num].arrivalTime)
        run_time = schedul_df[(schedul_df.process == f"P{num}")
                              & (schedul_df.state == "run")]

        finish_time = int(run_time.tail(1).finish)
        return_time = finish_time - arrival_time
        statistics_dict[f"P{num}"]["turn_around_time"] = return_time
        tmp.append(return_time)
    statistics_dict["average"]["turn_around_time"] = round(sum(tmp)/process_count, 2)

    # 응답 시간
    tmp = []
    for num in process_df.id.tolist():
        arrival_time = int(process_df[process_df.id == num].arrivalTime)

        run_time = schedul_df[(schedul_df.process == f"P{num}")
                              & (schedul_df.state == "run")]

        first_start_time = int(run_time.head(1).start)
        first_finish_time = int(run_time.head(1).finish)

        wait_time = first_start_time - arrival_time
        statistics_dict[f"P{num}"]["response_time"] = f"{wait_time} + ({first_start_time}~{first_finish_time})"
        tmp.append(wait_time)
    statistics_dict["average"]["response_time"] = f"{round(sum(tmp) / process_count, 2)} + ~"

    pandas_dict = {
        "process": [],
        "wait_sum": [],
        "turn_around_time": [],
        "response_time": [],
    }

    for key, value in statistics_dict.items():
        pandas_dict["process"].append(key)
        for col_name, data in value.items():
            pandas_dict[col_name].append(data)

    return pd.DataFrame.from_dict(pandas_dict)