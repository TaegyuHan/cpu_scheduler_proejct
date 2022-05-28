import plotly.express as px
from scheduler.first_come_first_served import FCFS
from scheduler.shortest_job_next import SJF
from scheduler.highest_response_ratio_next import HRN
from scheduler.round_robin import RR
from scheduler.shortest_remaining_time import SRT
from scheduler.non_preemptive_priority import NPS
from scheduler.preemptive_priority import PS


class TimeGanttPlot:
    """
        프로세스 스케줄링 시각화
    """
    MODLE = {
        'FCFS': FCFS(),
        'SJF': SJF(),
        'HRN': HRN(),
        'RR': RR(),
        'SRT': SRT(),
        'NPP': NPS(),
        'PP': PS()
    }

    @staticmethod
    def show_plot(logic_name: str):
        """ 원하는 로직에 맞춰서 시각화 보여주기 """

        model = TimeGanttPlot.MODLE[logic_name] # 모델 선택
        df = model.get_pandas_data_frame() # 데이터 프레임

        # 시각화 객체
        fig = px.timeline(df,
                          x_start="start",  # 시작
                          x_end="finish",  # 끝
                          y="process",  # y 축 데이터
                          title=model.NAME,  # 제목
                          color="state",  # 색
                          text="time"  # 라벨
                          )

        fig.layout.xaxis.type = 'linear' # x축 시간에서 숫자로 변경

        # state : run < 작동 기간 데이터

        try:
            fig.data[0].x = df["time"][df.state == model.STATE_RUN].tolist()
            # state : wait < 대기 시간 데이터
            fig.data[1].x = df["time"][df.state == model.STATE_WAIT].tolist()
        except IndexError: pass# 대기상태가 없는 경우

        fig.update_traces(textfont_size=14) # 프로세스 라벨 폰트 사이즈
        return fig


if __name__ == '__main__':
    TimeGanttPlot.show_plot("fcfs").show()