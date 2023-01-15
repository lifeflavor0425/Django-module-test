
""" 모듈 가져오기 """
import pandas as pd
# 지도 그리기 모듈
import folium
from folium.features import DivIcon
# 확률 계산 모듈 가져오기
from map import example
# DF 가져오기
subway_location = pd.read_excel("./map/public/all_station_line.xlsx")
reusult_df =pd.read_excel("./map/public/result_df.xlsx")
"""# 지도에 1~9호선 그리기"""
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
''' locations 초기화'''
def init():
    for idx in subway_location.index:
        lat = subway_location.loc[idx, "lat"]
        long = subway_location.loc[idx, "long"]
        line = subway_location.loc[idx, "subway"]
        locations[line].append([lat, long])

''' 노선 입력 -> 그 노선만 그리기'''
def make_map(input_line):
    tran_seoul_map = folium.Map(
        location=[37.566535, 126.9779692],  # 서울의 중심점(시청위치 혹은 구역의 중심)
        tiles="CartoDB dark_matter",  # 지도를 구성하는 타일의 종류 지정
        zoom_start=12,
        width=1200,
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

""" 확률 계산 """
def count_(input_line, input_time, tran_seoul_map):
    one_time_line_stations = []
    for line in line_stations[input_line]:
        if line not in one_time_line_stations:
            one_time_line_stations.append(line)
    # 확률 계산
    cal_per_dict = example.cal_per(input_line, input_time, one_time_line_stations, reusult_df)
    cal_per_cnt = 0
    for idx in reusult_df.index:  # 데이터 한개씩 뽑아서 역마다 점찍기
        lat = reusult_df.loc[idx, "lat"]
        long = reusult_df.loc[idx, "long"]
        line = reusult_df.loc[idx, "subway"]
        station = reusult_df.loc[idx, "station"]
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
                        <br> sum :  {cal_per_dict['sum'][cal_per_cnt]},
                        <br> sit_per : {cal_per_dict['sit_per'][cal_per_cnt]},
                        <br> person_per : {cal_per_dict['person_per'][cal_per_cnt]},
                        <br> per : {cal_per_dict['per'][cal_per_cnt]}
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

"""## 전체적으로 한번에 보기"""
def defalut_map():
    tran_seoul_map = folium.Map(
        location=[37.566535, 126.9779692],  # 서울의 중심점(시청위치 혹은 구역의 중심)
        tiles="CartoDB dark_matter",  # 지도를 구성하는 타일의 종류 지정
        zoom_start=12,
        width=1200,
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


# init() 실행
init()

"""지도 확인"""
# 지도 html 파일로 출력
# tran_seoul_map.save("./map.html")
