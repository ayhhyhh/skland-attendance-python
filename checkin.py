import skland
import requests
import os

# 读取 CRED UID
UID = os.environ.get("UID")
TOKEN = os.environ.get("TOKEN")
DINGTALKTOKEN = os.environ.get("DINGTALKTOKEN")

# 签到
account = skland.sklandAccount(TOKEN=TOKEN, UID=UID)
account.getGrantCode()
account.getCRED()
s = account.attendance()

# 发送钉钉消息
if DINGTALKTOKEN:
    DingTalkJSON = {
        "msgtype": "text",
        "text": {
            "content": f"森空岛\n{s}",
        },
    }

    url = f"https://oapi.dingtalk.com/robot/send?access_token={DINGTALKTOKEN}"
    DingTalkResponse = requests.post(url=url, json=DingTalkJSON)