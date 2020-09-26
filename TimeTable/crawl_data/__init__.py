import hashlib
import requests
from lxml import etree
import re

# 教务处登录网址
url = 'http://sso.jwc.whut.edu.cn/Certification/login.do'
# 请求标头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_user(username, password):
    # 加密后的用户名和密码参数
    username1 = hashlib.md5(username.encode('utf8')).hexdigest()
    temp = username + password
    password1 = hashlib.sha1(temp.encode('utf8')).hexdigest()

    # 根据webfinger的值用ajax异步获取得到code的值
    url_code = 'http://sso.jwc.whut.edu.cn/Certification/getCode.do'
    data_code = {
        'webfinger': '8eef3d54b38874b37897b6e29030365e'
    }
    code = requests.post(url=url_code, data=data_code).text
    # print(code)

    # 请求数据
    req_data = {
        'MsgID': '',
        'KeyID': '',
        'UserName': '',
        'Password': '',
        'rnd': '28679',
        'return_EncData': '',
        'code': code,
        'userName1': username1,
        'password1': password1,
        'webfinger': '8eef3d54b38874b37897b6e29030365e',
        'type': 'xs',
        'userName': username,
        'password': password
    }

    # 拿到教务处页面代码
    index_page = requests.post(url=url, data=req_data, headers=headers).text
    tree = etree.HTML(index_page)
    # 用户姓名
    name = tree.xpath("//div[@class='main-per-name']/p/b/text()")[0]
    user = {
        'name': name
    }
    return user


def get_data(username, password):
    # 加密后的用户名和密码参数
    username1 = hashlib.md5(username.encode('utf8')).hexdigest()
    temp = username + password
    password1 = hashlib.sha1(temp.encode('utf8')).hexdigest()

    # 根据webfinger的值用ajax异步获取得到code的值
    url_code = 'http://sso.jwc.whut.edu.cn/Certification/getCode.do'
    data_code = {
        'webfinger': '8eef3d54b38874b37897b6e29030365e'
    }
    code = requests.post(url=url_code, data=data_code).text
    # print(code)

    # 请求数据
    req_data = {
        'MsgID': '',
        'KeyID': '',
        'UserName': '',
        'Password': '',
        'rnd': '28679',
        'return_EncData': '',
        'code': code,
        'userName1': username1,
        'password1': password1,
        'webfinger': '8eef3d54b38874b37897b6e29030365e',
        'type': 'xs',
        'userName': username,
        'password': password
    }

    # 拿到教务处页面代码
    index_page = requests.post(url=url, data=req_data, headers=headers).text
    # 需要的数据
    data = []
    tree = etree.HTML(index_page)
    # print(user)
    # 课表
    table = tree.xpath("//tbody[@class='table-class-even']")[0]
    # 解析trs
    trs = table.xpath('./tr')
    # 利用count标记位置
    count = 0
    for tr in trs:
        # 解析每个td 并去掉那两个 上午 第一节
        tds = tr.xpath('./td[@style="text-align: center"]')
        for td in tds:
            # 标记位置
            count = count + 1
            divs = td.xpath('./div')
            if len(divs) != 0:
                for div in divs:
                    texts = div.xpath('./a//text()')
                    time = re.findall('\((.*?)\)', texts[3])[0]
                    week = re.findall('(第(.*?)周)', texts[3])[0]
                    # print(week)
                    # print(time)
                    data.append({
                        'lesson_name': texts[0].strip(),
                        'place': texts[1].strip(),
                        'week_num': week[1],
                        'week_desc': week[0],
                        'time_num': time[:-1],
                        'time_desc': time,
                        'count': count
                    })
                    # print(count)
    return data


# if __name__ == '__main__':
#     get_data('0121820390301', 'whlg201898.')
