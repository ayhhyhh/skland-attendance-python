import json
import sys
import time
import requests
import os
# 声明常量
# 签到url post请求
SIGN_URL = "https://zonai.skland.com/api/v1/game/attendance"
SUCCESS_CODE = 0
SLEEP_TIME = 3
FAIL_SIGN = False

# 读取 CRED UID
CRED = os.environ.get("CRED")
UID = os.environ.get("UID")
DINGTALKTOKEN = os.environ.get("DINGTALKTOKEN")


# 准备签到信息

headers = {
    "cred": CRED,
    "user-agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 25; ) Okhttp/4.11.0",
    "Content-Type": "application/json; charset=utf-8",
    "Accept-Encoding": "gzip",
    "Connection": "close",
    'platform': '1',
}

data = {
    "uid": UID,
    "gameId": 1,
}

# 签到请求
sign_response = requests.post(headers=headers, url=SIGN_URL, json=data)

# 检验返回是否为json格式
try:
    sign_response_json = json.loads(sign_response.text)
except:
    print(sign_response.text)
    print("返回结果非json格式, 请检查...")
    time.sleep(SLEEP_TIME)
    sys.exit()

# 如果为json则解析
code = sign_response_json.get("code")
message = sign_response_json.get("message")
data = sign_response_json.get("data")


# 返回成功的话，打印详细信息
if code == SUCCESS_CODE:
    print("签到成功")
    awards = sign_response_json.get("data").get("awards")
    s = ""
    for award in awards:
        s += (f"签到获得的奖励ID为: {award.get('resource').get('id')} \n")
        s += (f"此次签到获得了{award.get('count')}单位的{award.get('resource').get('name')} ({award.get('resource').get('type')})\n")
        s += (f"奖励类型为: {award.get('type')}")
    print(s)
else:
    if sign_response_json["message"] == "请勿重复签到！":
        s = "重复签到"
    elif sign_response_json["message"] == "用户未登录":
        FAIL_SIGN = True
        s = "CRED 已过期, 请更新 CRED secret."
    else:
        FAIL_SIGN = True
        s = str(sign_response_json)
    print(s)
    print("签到失败，请检查以上信息...")



if DINGTALKTOKEN:

    DingTalkJSON = {
        "msgtype": 'text',
        "text": {
            "content": f"森空岛\n{s}",
        },
    }

    url = f"https://oapi.dingtalk.com/robot/send?access_token={DINGTALKTOKEN}"
    DingTalkResponse = requests.post(url=url, json=DingTalkJSON)


class AbnormalChekinException(Exception):
    pass

if FAIL_SIGN:
    raise AbnormalChekinException("存在签到失败的账号，请检查信息")
else:
    print("程序运行结束")
