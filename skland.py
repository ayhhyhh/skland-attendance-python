# %%
import json
import time
import requests
import os
import hashlib
import hmac
from urllib import parse

SKLAND_AUTH_URL = r"https://as.hypergryph.com/user/oauth2/v2/grant"
CRED_CODE_URL = r"https://zonai.skland.com/api/v1/user/auth/generate_cred_by_code"
SKLAND_ATTENDANCE_URL = r"https://zonai.skland.com/api/v1/game/attendance"
APP_CODE = "4ca99fa6b56cc2ba"

header = {
    "User-Agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 31; ) Okhttp/4.11.0",
    "Accept-Encoding": "gzip",
    "Connection": "close",
}

# 签名请求头一定要这个顺序，否则失败
# timestamp是必填的,其它三个随便填,不要为none即可
header_for_sign = {"platform": "", "timestamp": "", "dId": "", "vName": ""}


class sklandAccount:
    def __init__(self, TOKEN, UID) -> None:
        self.TOKEN = TOKEN
        self.UID = UID
        self.header = header

    def getGrantCode(self):
        response = requests.post(
            SKLAND_AUTH_URL,
            json={"appCode": APP_CODE, "token": self.TOKEN, "type": 0},
            headers=self.header,
        )

        if response.status_code != 200:
            raise Exception(f"获得OAuth2 Grant Code失败: {response}")
        resp = response.json()
        if resp.get("status") != 0:
            raise Exception(f'获得OAuth2 Grant Code失败: {resp["msg"]}')

        self.GRANT = resp["data"]["code"]

    def getCRED(self):
        resp = requests.post(
            CRED_CODE_URL, json={"code": self.GRANT, "kind": 1}, headers=self.header
        ).json()

        if resp["code"] != 0:
            raise Exception(f'获得CRED失败: {resp["message"]}')
        self.CRED = resp["data"]["cred"]
        self.CRED_TOKEN = resp["data"]["token"]

    def signatureHeader(self, path, body_or_query):
        """
        获得签名头
        接口地址+方法为:
            GET: query, POST: body
            path + body/query + timestamp + 请求头的四个参数(dId, platform, timestamp, vName).toJSON()
        将此字符串做HMAC加密, 算法为SHA-256, 密钥token为CRED
        再将加密后的字符串做MD5即得到sign
        :param url: 请求路径(api url)
        :param body_or_query: 如果是GET, 则是它的query, POST则为它的body
        :return: 计算完毕的sign
        """
        # 总是说请勿修改设备时间, 怕不是yj你的服务器有问题吧, 所以这里特地-2
        timestamp = str(int(time.time()) - 2)
        token = self.CRED_TOKEN

        header_ca = json.loads(json.dumps(header_for_sign))
        header_ca["timestamp"] = timestamp
        header_ca_str = json.dumps(header_ca, separators=(",", ":"))

        s = path + body_or_query + timestamp + header_ca_str
        hex_s = hmac.new(
            token.encode("utf-8"), s.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        md5 = hashlib.md5(hex_s.encode("utf-8")).hexdigest()

        signedHeader = dict()
        signedHeader["cred"] = self.CRED

        for i in header:
            signedHeader[i] = self.header[i]

        signedHeader["sign"] = md5
        for i in header_ca:
            signedHeader[i] = header_ca[i]
        return signedHeader

    def attendance(self):
        body = {
            "gameId": 1,
            "uid": self.UID,
        }
        path = parse.urlparse(SKLAND_ATTENDANCE_URL).path
        signedHeader = self.signatureHeader(path, json.dumps(body))
        response = requests.post(SKLAND_ATTENDANCE_URL, headers=signedHeader, json=body)
        resp = response.json()
        if response.status_code != 200:
            raise Exception(f"签到失败: {resp}")
        if resp.get("code") != 0:
            raise Exception(f"签到失败: {resp}")

        print("签到成功")
        awards = resp.get("data").get("awards")
        s = ""
        for award in awards:
            s += f"签到获得的奖励ID为: {award.get('resource').get('id')} \n"
            s += f"此次签到获得了{award.get('count')}单位的{award.get('resource').get('name')} ({award.get('resource').get('type')})\n"
            s += f"奖励类型为: {award.get('type')}"
        print(s)

        return s
