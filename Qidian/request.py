import requests
from crypto import eninfo, ensign, make_post_data
import time

api_base = "https://druidv6.if.qidian.com/argus/api/v3/bookdetail/lookfor?"

def send_request(post_data: str, timestamp: int) -> None:
    info_template=f"T\x06\x04\x02\x03SR\x077c7d70b32de1efec100010519c06|7.9.434|720|1280|10000431|9|1|ASUS_I005DA|1736|10000431|4|0|{str(timestamp)}|0|d6423cb77c7d70b32de1efec100010519c06|9768b9e4bfcf6c35|||d6423cb77c7d70b32de1efec100010519c06|1\x01"
    sign_template=f"Rv1rPTnczce|{str(timestamp)}|0|d6423cb77c7d70b32de1efec100010519c06|1|7.9.434|0|{make_post_data(post_data)}|f189adc92b816b3e9da29ea304d4a7e4\x02\x02"
    cookie = f"ywkey=; ywguid=; appId=12; areaId=30; lang=cn; mode=normal; bar=36; qid=d6423cb77c7d70b32de1efec100010519c06; qidth=d6423cb77c7d70b32de1efec100010519c06; QDInfo={eninfo(info_template)}"
    headers = {
        'Cookie': cookie,
        'Qdsign': ensign(sign_template),
        'Tstamp': str(timestamp),
        'User-Agent': 'Mozilla / mobile QDReaderAndroid / 7.9.434 / 1736 / 10000431 / Asus / getTabHeight_68',
        'Qdinfo': eninfo(info_template)
    }
    print(headers)
    response = requests.request("Get", api_base + post_data, headers=headers)
    print(response.json())

if __name__ == "__main__":
    post_data = "bookId=1039457453&isOutBook=0"
    timestamp = int(time.time() * 1000)
    send_request(post_data, timestamp)