# 서울시 지하철 앉아 갈 수 있는 확률 구하기 프로젝트

# 데이터 수집
- 서울시열린공공데이터광장,공공데이터포털사이트참조
    - 서울시 지하철 호선별 역별 승하차 인원 정보 : (https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do)
    - 서울시 환승역 인원 정보 : (https://www.data.go.kr/data/15062858/fileData.do)
    - 서울시 역사 마스터 정보 : (https://www.data.go.kr/data/15099367/fileData.do)

# 데이터 시각화
## folium - 지도 라이브러리
- 전체 지하철 시각화
<img width="890" alt="스크린샷 2023-06-21 오후 10 19 43" src="https://github.com/lifeflavor0425/Django-module-test/assets/78671072/8a81afd1-9a54-409d-925a-9303aa1b748c">

- 입력한 호선 지하철 시각화
<img width="1037" alt="스크린샷 2023-06-21 오후 10 20 45" src="https://github.com/lifeflavor0425/Django-module-test/assets/78671072/cc726b1e-fe89-45d9-bdd6-10ce944bb077">

# 데이터 결과 분석
- 차량내부에있을때가역사에서차량을기다릴때보다앉을수있는확률이높을
것으로예상
<img width="1071" alt="스크린샷 2023-06-21 오후 10 23 14" src="https://github.com/lifeflavor0425/Django-module-test/assets/78671072/88648c46-ad99-4886-98ac-54ec13ea2055">

- 19시는 통상 퇴근 시간이고 퇴근하는 인구가 많을 것으로 예상
- 특정 시간대, 각 역별로 다르게 나옴, 유동인구가 많은 지하철역을 추론할 수 있을 
- 스타벅스 유동 인구 분석에서 시각화한 지도와 비교시 유동인구 밀집 지역을 유추할 수 있음
<img width="524" alt="스크린샷 2023-06-21 오후 10 29 28" src="https://github.com/lifeflavor0425/Django-module-test/assets/78671072/c5b865bc-5d73-43d3-b563-f057bb2c2063">

- 위와 비교해 봤을 때 유동인구가 많은 장소 == 스타벅스가 많은 장소에서는 지하철 앉을 확률이 극히 떨어짐을 알 수 있음

# Django 구현
- 지도
<img width="927" alt="스크린샷 2023-06-21 오후 10 21 03" src="https://github.com/lifeflavor0425/Django-module-test/assets/78671072/bd34d1bb-4f63-4e28-b9e3-ef2065cd72b9">

- 데이터 프레임 & 데이터 분석
<img width="1019" alt="스크린샷 2023-06-21 오후 10 22 11" src="https://github.com/lifeflavor0425/Django-module-test/assets/78671072/dcd6ad5d-9748-4937-97ac-222befc03655">

# 담당
- 데이터 전처리
- 데이터 시각화
- Django로 web 서비스 구현
