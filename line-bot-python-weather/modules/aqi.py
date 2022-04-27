import requests, json, statistics

def get_aqi(search_term):
    city_list = {}
    report = "找不到空氣品質資訊。"
    try:
        #  空氣品質報告API網址
        url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json'
        res = requests.get(url)
        data = res.json()
        record = data['records']
        for r in record:
            city, site, aqi, status = r['County'], r['SiteName'], r['AQI'], r['Status']
            if city not in city_list:
                city_list[city] = []
            city_list[city].append(aqi)
            if site == search_term:
                report = f"空氣品質: {status} ( AQI {aqi} )"
                break
            for i in city_list:
                if i in search_term:
                    int_aqi = [int(n) for n in city_list[i]]
                    aqi_value = round(statistics.mean(int_aqi))  # get average
                    aqi_status = ''
                    if aqi_value in range(0, 50+1):      aqi_status = '良好'
                    elif aqi_value in range(50, 100+1):  aqi_status = '普通'
                    elif aqi_value in range(100, 150+1): aqi_status = '不健康(對過敏體質)'
                    elif aqi_value in range(150, 200+1): aqi_status = '不健康'
                    elif aqi_value in range(200, 300+1): aqi_status = '非常不健康'
                    else:                                aqi_status = '危害'
                    report = f"空氣品質: {aqi_status} ( AQI {aqi_value} )"
                    break
        return report
    except:
        return report