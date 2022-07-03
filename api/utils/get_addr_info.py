import requests
import geoip2.database

# 爬取ip地址

ip = '194.55.0.1'
ip1 = '119.108.116.209'

ip_db = "../../static/ip_db/GeoLite2_City_db/GeoLite2-City.mmdb"

def get_addr_info(ip):
    if ip.startswith('10.') or ip.startswith('192.') or ip.startswith('172.'):
        return
    reader = geoip2.database.Reader(ip_db)
    data = reader.city(ip)
    print(data)
    print("IP Address: ", data.traits.ip_address)
    print("国家: ", data.country.names['zh-CN'])  # names['zh-CN']转换为中文
    print("省份: ", data.subdivisions.most_specific.names['zh-CN'])
    print("城市: ", data.city.names['zh-CN'])
    print("纬度: ", data.location.latitude)  # 位置
    print("经度: ", data.location.longitude)


if __name__ == '__main__':
    get_addr_info(ip)
