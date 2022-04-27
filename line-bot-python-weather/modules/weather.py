import requests, json

def get_weather(search_term):
    table = {}
    code = ''  # 你的資料授權碼
    result = "找不到天氣預報資訊。"
    try:
        url = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization={code}&downloadType=WEB&format=JSON'
        res = requests.get(url)
        data = res.json()
        location = data['cwbopendata']['dataset']['location']
        for i in location:
            city =      i['locationName']
            weather =   i['weatherElement'][0]['time'][0]['parameter']['parameterName']
            max_temp =  i['weatherElement'][1]['time'][0]['parameter']['parameterName']
            min_temp =  i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            rain_prob = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            table[city] = f'未來8小時: {weather}\n最高溫: {max_temp} °C\n最低溫: {min_temp} °C\n降雨機率: {rain_prob} %'
        for i in table:
            if i in search_term:
                result = table[i]
                break
        return result
    except:
        return result