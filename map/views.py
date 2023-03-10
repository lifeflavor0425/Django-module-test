from django.shortcuts import render, redirect
from map.modules.make_map import make_map, defalut_map, count_
import pandas as pd
import json

# Create your views here.
def index(request):
    map = defalut_map()
    maps = map._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

    return render(request, "map/index.html", {"map": maps})


def station_line_search(request):
    print(request.POST.get("search_line"), request.POST.get("search_time"))
    input_line = request.POST.get("search_line")
    input_time = request.POST.get("search_time")
    if input_line == "노선선택" or input_time == "시간선택":
        map = defalut_map()
        maps = map._repr_html_()
    else:
        map = make_map(input_line)
        map = count_(input_line, input_time, map)
        maps = map._repr_html_()
    return render(request, "map/index.html", {"map": maps})


def None_404(request):
    return render(
        request,
        "map/404.html",
    )


def charts(request):
    return render(
        request,
        "map/charts.html",
    )


def table(request):
    result_df = pd.read_excel("./map/public/result_df.xlsx")
    result_df = result_df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])
    return render(request, "map/table.html", {"result_df": result_df})
