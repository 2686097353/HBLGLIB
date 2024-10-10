import requests
from urllib.parse import urlparse, parse_qs
import json
import time

config = {
    "user": 202220291304,#你的账号
    "pw": "192947401ba2cd9c04331e056d00ee856895f441d5e07fdfac400711cd04c9c3d953f52",#加密的密码
    "seat": "T1-1-005",#座位号
    "StartTime": "07:00:00",
    "EndTime": "22:00:00",
}


# 1. 登录获取ticket
def get_ticket(user, pw):
    url = "https://cas.hbpu.edu.cn/lyuapServer/v1/tickets"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Referer": "https://cas.hbpu.edu.cn/lyuapServer/login?service=http://zwyd.hbpu.edu.cn",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {
        "username": user,
        "password": pw,
        "service": "http://zwyd.hbpu.edu.cn",
        "loginType": "",  # 请根据实际情况提供loginType的值
        'id': '',
        'code': '',
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # 如果请求失败则抛出异常

    json_response = response.json()
    tgt = json_response['tgt']
    ticket = json_response['ticket']

    print(json_response)

    print(f"Ticket: {ticket}")
    print(f"TGT: {tgt[11:]}")
    return ticket, tgt


# 2. 用ticket获取新的定向网址
def get_auth_address(ticket):
    url = 'http://zwyd.hbpu.edu.cn/ic-web/auth/address'
    params = {
        'finalAddress': 'http://zwyd.hbpu.edu.cn',
        'errPageUrl': 'http://zwyd.hbpu.edu.cn/#/error',
        'manager': 'false',
        'consoleType': '16',
        'queryParam': f'?ticket={ticket}#/'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # 如果请求失败则抛出异常

    return response.json()["data"]


# 3. 从 定向网址 中提取 redirectUrl 和 extInfo
def extract_redirect_and_extinfo(auth_address):
    # 解析 URL
    parsed_url = urlparse(auth_address)
    # 获取查询参数
    query_params = parse_qs(parsed_url.query)

    # 打印查询参数以供调试
    print("Parsed Query Params:", query_params)

    # 提取 redirectUrl 和 extInfo
    redirect_url = query_params.get('redirectUrl', [None])[0]
    ext_info = query_params.get('extInfo', [None])[0]

    if not redirect_url or not ext_info:
        raise ValueError("Required parameters not found in URL.")

    return redirect_url, ext_info


# 4. 重定向到登录页面
def redirect_to_login_page(redirectUrl, extInfo):
    url = 'http://zwyd.hbpu.edu.cn/authcenter/toLoginPage'
    params = {
        'redirectUrl': redirectUrl,
        'extInfo': extInfo,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    response.raise_for_status()  # 如果请求失败则抛出异常

    if response.status_code == 302:
        return response.headers.get('Location')
    else:
        raise Exception('Failed to redirect to login page')


# 提取 doAuth
def extract_do_auth(url):
    # 解析 URL
    parsed_url = urlparse(url)

    # 获取查询参数
    query_params = parse_qs(parsed_url.query)

    # 提取 'service' 参数的值
    service_url = query_params.get('service', [None])[0]

    if not service_url:
        raise ValueError("Service parameter not found in URL.")

    # 提取 doAuth 部分
    service_path = urlparse(service_url).path
    path_segments = service_path.split('/')

    # 查找 doAuth 的部分
    if len(path_segments) > 3:
        do_auth = path_segments[3]
        return do_auth
    else:
        raise ValueError("doAuth parameter not found in service URL.")


# 使用 doAuth组成新的定向
def perform_auth(ticket, do_auth_id):
    # 构造请求的 URL
    url = f'http://zwyd.hbpu.edu.cn/authcenter/doAuth/{do_auth_id}'
    params = {
        'ticket': ticket
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    # 发起 GET 请求
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    # 处理响应
    if response.status_code == 302:
        redirect_url = response.headers.get('Location')
        return redirect_url
    else:
        raise Exception('Authentication failed or unexpected response.')


# 从给定的 URL 中提取 `uuid`, `uniToken`, 和 `extInfo` 参数。
def extract_params_from_url(url):
    """
    :param url: 包含查询参数的 URL
    :return: 提取的 `uuid`, `uniToken`, 和 `extInfo`
    """
    # 解析 URL
    parsed_url = urlparse(url)

    # 获取查询参数
    query_params = parse_qs(parsed_url.query)

    # 提取各个参数
    uuid = query_params.get('uuid', [None])[0]
    uni_token = query_params.get('uniToken', [None])[0]
    ext_info = query_params.get('extInfo', [None])[0]

    return uuid, uni_token, ext_info


#发起 GET 请求并获取响应中的 Set-Cookie 头部。
def get_set_cookie(uuid, uniToken, extInfo):
    try:
        url = "http://zwyd.hbpu.edu.cn/ic-web//auth/token"
        params = {
            "uuid": uuid,
            "uniToken": uniToken,
            "extInfo": extInfo,
        }
        headers = {
            "Host": "zwyd.hbpu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }

        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        # 获取 Set-Cookie 头部
        set_cookie = response.headers.get('Set-Cookie')
        return set_cookie

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


# 解析ic-cookie
def extract_ic_cookie(cookie_header):
    # 查找 'ic-cookie=' 的起始位置
    start = cookie_header.find('ic-cookie=')

    if start == -1:
        return None  # 如果未找到 'ic-cookie=', 返回 None

    # 查找 '=' 后的值
    start += len('ic-cookie=')
    end = cookie_header.find(';', start)

    if end == -1:
        end = len(cookie_header)  # 如果没有结束分号，则直到字符串末尾

    # 返回包含 'ic-cookie=' 和其值的字符串
    return f"ic-cookie={cookie_header[start:end]}"


# 获取用户信息
def fetch_user_info(cookie):
    url = "http://zwyd.hbpu.edu.cn/ic-web/auth/userInfo"
    headers = {
        "Host": "zwyd.hbpu.edu.cn",
        "Accept": "application/json, text/plain, */*",
        "lan": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Referer": "http://zwyd.hbpu.edu.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookie,
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析 JSON 内容
        json_response = response.json()
        return json_response

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        return None


# 时间配置（自动加一天）
def get_time(start_time, end_time):
    now = time.time() + 86400
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d ", timeArray)
    resvBeginTime = otherStyleTime + str(start_time)
    resvEndTime = otherStyleTime + str(end_time)
    return resvBeginTime, resvEndTime


#抢座位函数
def reservation(cookie, resvMember, start_time, end_time, resv_dev):
    url = 'http://zwyd.hbpu.edu.cn/ic-web/reserve'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '224',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cookie,
        'Host': 'zwyd.hbpu.edu.cn',
        'Lan': '1',
        'Origin': 'http://zwyd.hbpu.edu.cn',
        'Token': 'ad338b8180c549099d855002f3a78e16',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
    }

    data = {
        "sysKind": 8,
        "appAccNo": resvMember,  # 个人编号
        "memberKind": 1,
        "resvMember": [
            resvMember
        ],  # 个人编号
        "resvBeginTime": start_time,  # 开始时间
        "resvEndTime": end_time,  # 结束时间
        "testName": "",
        "captcha": "",
        "resvProperty": 0,
        "resvDev": [
            resv_dev
        ],  # 座位号
        "memo": ""
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查是否有请求异常
        json_response = response.json()
        return json_response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")


if __name__ == '__main__':
    try:

        json_data = config

        # 访问字典中的数据
        get_ticket_user = json_data['user']
        get_ticket_pw = json_data['pw']
        seat = json_data['seat']
        start_time = json_data['StartTime']
        end_time = json_data['EndTime']

        ticket, tgt = get_ticket(get_ticket_user, get_ticket_pw)
        auth_address = get_auth_address(ticket)
        print(f"auth_address: {auth_address}")

        redirectUrl, ext_info = extract_redirect_and_extinfo(auth_address)
        print(f"redirectUrl: {redirectUrl}")
        print(f"ext_info: {ext_info}")

        login_page_url = redirect_to_login_page(redirectUrl, ext_info)
        print(f"Login Page URL: {login_page_url}")

        do_auth = extract_do_auth(login_page_url)
        print(f"doAuth: {do_auth}")

        redirect_url = perform_auth(ticket, do_auth)
        print(f"Redirect URL: {redirect_url}")

        uuid, uni_token, ext_info = extract_params_from_url(redirect_url)

        print(f"uuid: {uuid}\nuni_token:{uni_token}\next_info:{ext_info}\n")

        set_cookie = get_set_cookie(uuid, uni_token, ext_info)
        print(f"Set-Cookie: {set_cookie}")

        set_cookie = extract_ic_cookie(set_cookie)
        print(f"Set-Cookie: {set_cookie}")

        print('\n' * 10, '-' * 40, '\n')

        user_info = fetch_user_info(set_cookie)
        print(f"user_info: {user_info}")

        user_data = user_info["data"]
        trueName = user_data["trueName"]
        logonName = user_data["logonName"]
        accNo = user_data["accNo"]  # 个人编号
        print(trueName, logonName, accNo, "登录成功")



        start_time, end_time = get_time(start_time, end_time)

        # 获取座位编号
        with open('seat.json', 'r') as file:
            seat_data = json.load(file)
        resv_dev = seat_data[seat]

        print("预约开始时间：", start_time, "\n预约结束时间：", end_time, "\n座位：", resv_dev, seat)
        reservation_json = reservation(set_cookie, accNo, start_time, end_time, resv_dev)
        print(reservation_json)

        print('\n', '-' * 40, '\n')



    except Exception as e:
        print(f"Error: {e}")
