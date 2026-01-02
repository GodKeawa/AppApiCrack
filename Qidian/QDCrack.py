import time
import hashlib
import operator
from functools import reduce
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
import urllib.parse
import binascii

# --- 设备和应用配置 (来自 QDLogin.py) ---
os_uuid = '866174010680719'
os_imei = os_uuid
os_qimei = '866174010680719'
os_android_version = '5.1.1'
os_device_type = 'OPPO _OPPO R11'
os_version_1 = '1794'
os_dim = '1080'
devicename = 'Nexus 6'
devicetype = 'OPPO _OPPO R11'
app_versioncode = '418'
app_versionname = '7.9.14'
source = '1000017' # 用于 QDInfo 的 source

# 假设原 my_base64 是一个特殊的 Base64 实现，此处替换为标准的 base64.b64encode
# 并在最后移除 Python 默认添加的换行符
def custom_base64_encode(input_bytes):
    """使用标准的Base64编码，这与原始的my_base64可能略有不同。"""
    encoded = base64.b64encode(input_bytes)
    return encoded.decode('utf-8').replace('\n', '')

# 为了最大限度还原原始逻辑，这里我们暂时使用标准 base64，如果遇到问题，
# 则需要手动实现原始文件的 my_base64 逻辑。

def pkcs7_padding(data):
    """实现PKCS#7填充，与原始代码中的逻辑一致。"""
    block_size = 8  # DES/3DES 的块大小
    padding_len = block_size - (len(data) % block_size)
    # 填充字节是填充长度本身
    padding = bytes([padding_len]) * padding_len
    return data + padding


def get_qd_info_python(app_usertoken='0'):
    # 1. 构造明文 (Data String)
    timestamp = str(int(time.time() * 1000))
    data_str = f"{os_uuid}|{app_versionname}|{os_dim}|{os_version_1}|{source}|{os_android_version}|1|{os_device_type}|{app_versioncode}|{source}|4|{app_usertoken}|{timestamp}|1|{os_qimei}"
    plain_text = data_str.encode('utf-8')

    # 2. 密钥和IV
    # 原始密钥 16 字节 (Two-Key 3DES K1 K2)
    key_str = "0821CAAD409B8402"
    key_bytes = binascii.unhexlify(key_str)  # 将16进制字符串转为字节

    # 扩展为 24 字节 (K1 K2 K1)
    full_key = key_bytes + key_bytes[:8]

    # 假设 IV 为全零
    iv = b'\x00' * 8

    # 3. 加密操作
    # 填充
    padded_data = pkcs7_padding(plain_text)

    # 3DES EDE CBC 加密
    cipher = Cipher(algorithms.TripleDES(full_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()

    # 4. Base64 编码
    return custom_base64_encode(encrypted_bytes)


def get_qd_sign_python(postdata="", usertoken='0'):
    # 1. 构造明文的各个部分
    src = 'Rv1rPTnczce'
    timestamp = str(int(time.time() * 1000))
    uuid = os_uuid
    version_name = app_versionname
    version_a = '0'  # 硬编码

    # 硬编码的 signatures 字符串
    signatures_str = '308204a830820390a003020102020900936eacbe07f201df300d06092a864886f70d0101050500308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d301e170d3038303232393031333334365a170d3335303731373031333334365a308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d30820120300d06092a864886f70d01010105000382010d00308201080282010100d6931904dec60b24b1edc762e0d9d8253e3ecd6ceb1de2ff068ca8e8bca8cd6bd3786ea70aa76ce60ebb0f993559ffd93e77a943e7e83d4b64b8e4fea2d3e656f1e267a81bbfb230b578c20443be4c7218b846f5211586f038a14e89c2be387f8ebecf8fcac3da1ee330c9ea93d0a7c3dc4af350220d50080732e0809717ee6a053359e6a694ec2cb3f284a0a466c87a94d83b31093a67372e2f6412c06e6d42f15818dffe0381cc0cd444da6cddc3b82458194801b32564134fbfde98c9287748dbf5676a540d8154c8bbca07b9e247553311c46b9af76fdeeccc8e69e7c8a2d08e782620943f99727d3c04fe72991d99df9bae38a0b2177fa31d5b6afee91f020103a381fc3081f9301d0603551d0e04160414485900563d272c46ae118605a47419ac09ca8c113081c90603551d230481c13081be8014485900563d272c46ae118605a47419ac09ca8c11a1819aa48197308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d820900936eacbe07f201df300c0603551d13040530030101ff300d06092a864886f70d010105050003820101007aaf968ceb50c441055118d0daabaf015b8a765a27a715a2c2b44f221415ffdace03095abfa42df70708726c2069e5c36eddae0400be29452c084bc27eb6a17eac9dbe182c204eb15311f455d824b656dbe4dc2240912d7586fe88951d01a8feb5ae5a4260535df83431052422468c36e22c2a5ef994d61dd7306ae4c9f6951ba3c12f1d1914ddc61f1a62da2df827f603fea5603b2c540dbd7c019c36bab29a4271c117df523cdbc5f3817a49e0efa60cbd7f74177e7a4f193d43f4220772666e4c4d83e1bd5a86087cf34f2dec21e245ca6c2bb016e683638050d2c430eea7c26a1c49d3760a58ab7f1a82cc938b4831384324bd0401fa12163a50570e684d'

    postdata_md5 = hashlib.md5(postdata.encode('utf-8')).hexdigest()
    signatures_md5 = hashlib.md5(signatures_str.encode('utf-8')).hexdigest()

    # 构造 DES 加密需要的明文 (Plain Text)
    plain_text_str = f"{src}|{timestamp}|{usertoken}|{uuid}|1|{version_name}|{version_a}|{postdata_md5}|{signatures_md5}"
    plain_text = plain_text_str.encode('utf-8')

    # 2. 密钥和IV
    # 密钥 '7B3164596771452968392C5229684B71456376345D6B5B68' (24字节，64个16进制字符)
    key_hex = '7B3164596771452968392C5229684B71456376345D6B5B68'
    key = binascii.unhexlify(key_hex)

    # IV '3031323334353637' (8字节，16个16进制字符)
    iv_hex = '3031323334353637'
    iv = binascii.unhexlify(iv_hex)

    # 3. 加密操作
    # 填充
    padded_data = pkcs7_padding(plain_text)

    # 3DES EDE CBC 加密
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()

    # 4. Base64 编码
    return custom_base64_encode(encrypted_bytes)

if __name__ == "__main__":
    # 假设 postdata 是登录请求的 URL 参数字符串
    login_postdata = 'appid=12&areaid=30&autotime=30&code=&devicename=Nexus+6&devicetype=OPPO+_OPPO+R11&format=json&imei=866174010680719&loginType=23&osversion=Android5.1.1_7.9.14_418&password=1212aaq&qimei=866174010680719&referer=http%3A%2F%2Fandroid.qidian.com&returnurl=http%3A%2F%2Fwww.qidian.com&sdkversion=201&source=1000017&ticket=0&username=xuelong1012&version=418'
    usertoken_example = '0'  # 初始登录时 usertoken 通常为 '0'

    # 生成 QDInfo
    qd_info = get_qd_info_python(app_usertoken=usertoken_example)
    print(f"Generated QDInfo: {qd_info}")

    # 生成 QDSign
    qd_sign = get_qd_sign_python(postdata=login_postdata, usertoken=usertoken_example)
    print(f"Generated QDSign: {qd_sign}")