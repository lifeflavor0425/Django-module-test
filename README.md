# **이건우 파트 (확률 구하기 및 시각화) [ 웹 부분은 별도 파일 참조 ]**


## 1) 프로그램 작동 가능 부분

### 1-1) 모듈 가져오기


import pandas as pd
import re
# 지도 그리기 모듈
import folium
from folium.features import DivIcon


### 1-2) 데이터프레임 가져오기

# DF 가져오기
subway_location = pd.read_excel("/content/drive/MyDrive/SK_Rookies/모듈프로젝트1/data/all_station_line.xlsx")

# all_train_info DF
all_train_info = pd.read_excel("/content/drive/MyDrive/SK_Rookies/모듈프로젝트1/data/all_train_info.xlsx")

### 1-3) 데이터프레임 정제 + 최종 데이터프레임 생성

all_train_info = all_train_info.rename(columns={"line": "subway"})
all_train_info["subway"] = all_train_info["subway"].apply(lambda x: f"{x}호선")
all_train_info["station"] = all_train_info["station"].apply(lambda x: re.sub(r"\([^)]*\)", "", x))
all_train_info["if_tf"] = all_train_info["if_tf"].apply(lambda x: int(x))
# 최종 DF
result_df = pd.merge(
    subway_location, all_train_info, on=["subway", "station", "if_tf"], how="left"
)
result_df = result_df.drop(columns=["level_0", "train_cnt"])
result_df = result_df.drop_duplicates(["subway", "station", "if_tf"])
result_df.to_excel("./result_df.xlsx")

### 1-4) 확률 계산 함수

def cal_per(line, time, line_stations, all_train_info):

    li_sum = []
    li_sit_per = []
    li_person_per = []
    li_per = []

    sum = 0  # 차량 내의 인원 초기화

    # 호선의 첫번째부터 연산
    for line_station in line_stations:
        # 주어진 호선과 역명에 맞는 데이터 시리즈 받아오기
        tmp = all_train_info[
            (all_train_info.station == line_station) & (all_train_info.subway == line)
        ]
        in_num = tmp[f"in_{time}"].item()  # 탑승인원
        out_num = tmp[f"out_{time}"].item()  # 하차인원
        in_tf_num = tmp[f"tf_in_{time}"].item()  # (환승 후) 탑승인원
        out_tf_num = tmp[f"tf_out_{time}"].item()  # (환승 후) 하차인원
        sit_cnt = tmp["sit_cnt"].item()  # 사용 가능한 좌석 수
        person_cnt = tmp["person_cnt"].item()  # 적정한 탑승 승객 인원 수

        # 차량 탑승시 앉아 갈 수 있는 확률
        if sum < 0:
            sum_tmp = 0  # 노선 전체를 계산 할 때는 오차를 허용할 수 있지만 인원을 파악하려면 음수가 나와서는 안됨
        else:
            sum_tmp = sum
        if tmp.if_tf.item():
            last = sum_tmp - out_num - out_tf_num  # 차량안에 남는사람
            if last < 0:
                last = 0
            can_sit = sit_cnt - last  # 남아있는 좌석 수
        else:
            last = sum_tmp - out_num  # 차량안에 남는사람
            if last < 0:
                last = 0
            can_sit = sit_cnt - last  # 남아있는 좌석 수
        if can_sit > 0:  # 앉아 갈 수 있는 좌석이 남았을 때
            sit_per = (can_sit / sit_cnt) * 100
        else:
            sit_per = 0

        # 차량 내부에 있는데 내 주변 의자가 비어있을 확률 (자리 순환률 [얼마나 사람들이 일어나서 나갈 것인가] )
        if sum_tmp <= 0:
            per = 100
        else:
            if tmp.if_tf.item():
                per = ((out_num + out_tf_num) / sum_tmp) * 100  # 차량안에 있는 사람이 나갈 확률
                if per > 100:
                    per = 100
            else:
                per = ((out_num) / sum_tmp) * 100  # 차량안에 있는 사람이 나갈 확률
                if per > 100:
                    per = 100

        # 현 역에서 차량에 탑승하고 있는 전체 인원 계산
        if tmp.if_tf.item():
            # 환승가능한 역의 갯수 받아오기
            transfer_cnt = tmp.tf_cnt.item()
            # 현재 타고있는 인원 계산 공식
            sum = sum + (in_num + in_tf_num - out_num - out_tf_num) / transfer_cnt
        else:
            # 현재 타고있는 인원 계산 공식
            sum = sum + in_num - out_num

        # 적정 탑승 인원과 비교한 차량 내부 혼잡도
        if sum < 0:
            person_per = 0
        else:
            person_per = (sum / person_cnt) * 100

        li_sum.append(sum)
        li_sit_per.append(sit_per)
        li_person_per.append(person_per)
        li_per.append(per)

    return {
        "sum": li_sum,
        "sit_per": li_sit_per,
        "person_per": li_person_per,
        "per": li_per,
    }


#################################################################################################
# line = 8            # 호선
# time = '12'         # 시간
# line_stations = ['암사', '천호(풍납토성)', '강동구청',
#                  '몽촌토성(평화의문)', '잠실(송파구청)',
#                  '석촌', '송파', '가락시장', '문정', '장지',
#                  '복정', '산성', '남한산성입구(성남법원.검찰청)',
#                  '단대오거리', '신흥', '수진', '모란']

#                     # 해당 호선의 순서


# print(cal_per(line, time, line_stations, all_train_info))


### 1-5) 초기화 함수

# 노선 색
fill_color = {
    "1호선": "#0052A4",
    "2호선": "#00A84D",
    "3호선": "#EF7C1C",
    "4호선": "#00A5DE",
    "5호선": "#996CAC",
    "6호선": "#CD7C2F",
    "7호선": "#747F00",
    "8호선": "#E6186C",
    "9호선": "#BB8336",
}
# 위치 dic // 노선별 역 dic
locations = {f"{i}호선": [] for i in range(1, 10)}
line_stations = {f"{i}호선": [] for i in range(1, 10)}

""" locations 초기화"""


def init():
    for idx in subway_location.index:
        lat = subway_location.loc[idx, "lat"]
        long = subway_location.loc[idx, "long"]
        line = subway_location.loc[idx, "subway"]
        locations[line].append([lat, long])



init()

### 1-6) 입력 값 없을 때 ( 모든 노선 그리기) 함수

def defalut_map():
    tran_seoul_map = folium.Map(
        location=[37.566535, 126.9779692],  # 서울의 중심점(시청위치 혹은 구역의 중심)
        tiles="CartoDB dark_matter",  # 지도를 구성하는 타일의 종류 지정
        zoom_start=12,
        width=1400,
        height=800,
    )
    for idx in subway_location.index:  # 데이터 한개씩 뽑아서 역마다 점찍기
        lat = subway_location.loc[idx, "lat"]
        long = subway_location.loc[idx, "long"]
        line = subway_location.loc[idx, "subway"]
        ten_color = "white"

        if subway_location.loc[idx, "if_tf"]:
            ten_color = "yellow"

        folium.CircleMarker(  # 역마다 표시
            location=[lat, long],
            fill=True,
            fill_color=ten_color,
            fill_opacity=1,
            color=ten_color,
            weight=1,
            radius=5,
        ).add_to(tran_seoul_map)

    lines = subway_location.groupby("subway").count().index  # 각 호선 리스트
    for line in lines:  # 호선 역 마다 선  긋기
        folium.PolyLine(
            locations=locations[line], tooltip=f"{line}", color=fill_color[line], weight=5
        ).add_to(tran_seoul_map)
    return tran_seoul_map


### 1-7) 입력 값 있을 때 (입력한 노선만 그리기) 함수

def make_map(input_line):

    tran_seoul_map = folium.Map(
        location=[37.566535, 126.9779692],  # 서울의 중심점(시청위치 혹은 구역의 중심)
        tiles="CartoDB dark_matter",  # 지도를 구성하는 타일의 종류 지정
        zoom_start=12,
        width=1400,
        height=800,
    )

    for idx in subway_location.index:  # 데이터 한개씩 뽑아서 역마다 점찍기
        lat = subway_location.loc[idx, "lat"]
        long = subway_location.loc[idx, "long"]
        line = subway_location.loc[idx, "subway"]
        station = subway_location.loc[idx, "station"]
        ten_color = "white"
        if subway_location.loc[idx, "if_tf"]:
            ten_color = "yellow"

        if input_line == line:  # 입력한 노선만 점 찍기
            line_stations[line].append(station)
            folium.CircleMarker(  # 역마다 표시
                location=[lat, long],
                fill=True,
                fill_color=ten_color,
                fill_opacity=1,
                color=ten_color,
                weight=1,
                radius=5,
            ).add_to(tran_seoul_map)

            folium.PolyLine(  # 해당 노선만 그리기
                locations=locations[line], tooltip=f"{line}", color=fill_color[line], weight=5
            ).add_to(tran_seoul_map)
    return tran_seoul_map


### 1-8) 확률 계산 적용 -> 각 역마다 결과값 반환

def count_(input_line, input_time, tran_seoul_map):
    one_time_line_stations = []
    for line in line_stations[input_line]:
        if line not in one_time_line_stations:
            one_time_line_stations.append(line)
    # 확률 계산
    cal_per_dict = cal_per(input_line, input_time, one_time_line_stations, result_df)
    cal_per_cnt = 0
    for idx in result_df.index:  # 데이터 한개씩 뽑아서 역마다 점찍기
        lat = result_df.loc[idx, "lat"]
        long = result_df.loc[idx, "long"]
        line = result_df.loc[idx, "subway"]
        station = result_df.loc[idx, "station"]
        if input_line == line:  # 입력한 노선만 점 찍기
            folium.Marker(  # 역마다 마커 표시
                location=[lat, long],
                popup="<b>subway</b>",
                tooltip=f"""
                <div 
                    style= 
                        'background-color : white;color:balck;
                        font-size : 16px; 
                        font-weight:700; 
                        height : auto;'
                        >{station} 
                        <br> 시간 : {input_time}시
                        <br> 누적인원 :  {round(cal_per_dict['sum'][cal_per_cnt])} ,
                        <br> 혼잡도 : {round(cal_per_dict['person_per'][cal_per_cnt], 2)}% ,
                        <br> 앉을 확률 : {round(cal_per_dict['per'][cal_per_cnt], 2)}%
                </div>
                """,
                icon=DivIcon(  # 마커를 텍스트로 변경
                    icon_size=(100, 50),
                    icon_anchor=(-10, -10),
                    html=f"<div style= 'color:white; font-size : 15px; font-weight:700; height : 14px'>{station} </div>",
                ),
            ).add_to(tran_seoul_map)
            cal_per_cnt += 1

    return tran_seoul_map


### 1-9) Django에서 활용 부분(views.py)

'''
  **처음 홈-페이지 함수**
'''
def index(request):
    map = defalut_map()
    maps = map._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

    return map
    # return render(request, "map/index.html", {"map": maps}) -> Django에서 사용

map = index('request')

map

'''
  **입력값을 전송하면 호출되는 함수**
  입력값 있을 때 -> make_map()함수 호출
  입력값 없을 때 or 기본 값인 '노선선택'이나 '시간선택'으로 입력했을 때 -> defalut_map()함수 호출
'''
def station_line_search(request):
    # 실제 데이터 전송시 사용
    # input_line = request.POST.get("search_line")
    # input_time = request.POST.get("search_time")

    # 임시 입력값
    input_line = input('노선선택 \t\t')
    input_time = input('시간선택 \t\t')
    if input_line == "노선선택" or input_time == "시간선택":
        map = defalut_map()
        maps = map._repr_html_()
    else:
        map = make_map(input_line)
        map = count_(input_line, input_time, map)
        maps = map._repr_html_()
    return map
    # return render(request, "map/index.html", {"map": maps})

map2 = station_line_search('request')


map2
