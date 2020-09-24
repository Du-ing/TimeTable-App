import hashlib
import requests

# 教务处登录网址
url = 'http://sso.jwc.whut.edu.cn/Certification/login.do'
# 请求标头
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

def get_lesson(username,password):
    # 加密后的用户名和密码参数
    username1 = hashlib.md5(username.encode('utf8')).hexdigest()
    temp = username + password
    password1 = hashlib.sha1(temp.encode('utf8')).hexdigest()

    # 根据webfinger的值用ajax异步获取得到code的值
    url_code = 'http://sso.jwc.whut.edu.cn/Certification/getCode.do'
    data_code = {
        'webfinger': '8eef3d54b38874b37897b6e29030365e'
    }
    code = requests.post(url=url_code,data=data_code).text
    # print(code)

    # 请求数据
    data = {
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

    index_page = requests.post(url=url,data=data,headers=headers).text
    with open('../page/index.html','w',encoding='utf-8') as fp:
        fp.write(index_page)
        fp.close();


if __name__ == '__main__':
    get_lesson('xxxxxx','xxxxxx')