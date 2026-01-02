import base64
import binascii
import hashlib

from Crypto.Cipher import DES3
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES

def uninfo(s):
    key = b'0821CAAD409B8402'
    data = base64.b64decode(s)
    cryptor = DES3.new(key, DES3.MODE_CBC, b'00000000')
    print(cryptor.decrypt(data))
    return cryptor.decrypt(data)

def eninfo(s):
    key = b'0821CAAD409B8402'
    cryptor = DES3.new(key, DES3.MODE_CBC, b'00000000')
    data = s.encode('utf-8')
    print(base64.b64encode(cryptor.encrypt(data)))
    return base64.b64encode(cryptor.encrypt(data))

def unsign(s):
    key_hex = '7B3164596771452968392C5229684B71456376345D6B5B68'
    key = binascii.unhexlify(key_hex)

    iv_hex = '3031323334353637'
    iv = binascii.unhexlify(iv_hex)

    # 3DES EDE CBC 加密
    cipher = Cipher(TripleDES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    data = base64.b64decode(s)
    decrypted_bytes = decryptor.update(data) + decryptor.finalize()
    print(decrypted_bytes)
    return decrypted_bytes

def ensign(s):
    key_hex = '7B3164596771452968392C5229684B71456376345D6B5B68'
    key = binascii.unhexlify(key_hex)

    iv_hex = '3031323334353637'
    iv = binascii.unhexlify(iv_hex)

    # 3DES EDE CBC 加密
    cipher = Cipher(TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    data = s.encode('utf-8')
    encrypted_bytes = encryptor.update(data) + encryptor.finalize()
    result = base64.b64encode(encrypted_bytes).decode('utf-8')
    padd_result = ""
    for i in range(len(result) // 60 + 1):
        padd_result = padd_result + result[i * 60:(i + 1) * 60] + " "
    print(padd_result)
    return padd_result.encode('utf-8')

def make_post_data(postdata=''):
    postdataMD5 = hashlib.md5(postdata.lower().encode(encoding='utf-8')).hexdigest()
    print(postdataMD5)
    return postdataMD5

if __name__ == '__main__':
    uninfo("b4nNNPe0FfY7XgDyiz8rayu8FK3ZeUBW1GpBi3VnQHVDDmF81eKT4x9LcvX+2G/j0SYp12TPPh/Tnz5qZnGLEiE7rQ8nMSQOUIRIKPY5Lp2N7vjxPk9Sklh/2nrYz+J8L65FzpTeWPC5m7spHtettJ17iq4FY3uQCVCxYuS+UKUy7WSTyoaSXYvmqelyBzV4r8uv2Yt4SPgCnsBjgOmnNJhhvni1vxOeus4HAvpiztm8OmBEIanNWuc9yBwhhMjrx2R4yf5S2hjKr9VaNHBXVg==")
    uninfo("b4nNNPe0FfY7XgDyiz8rayu8FK3ZeUBW1GpBi3VnQHVDDmF81eKT4x9LcvX+2G/j0SYp12TPPh/Tnz5qZnGLEiE7rQ8nMSQOUIRIKPY5Lp2N7vjxPk9Sklh/2nrYz+J8cmftvqRaiX8kZogZAJU9iRMLMAy0ysCf3NZTjgfXP8JtPVo5WrbHEZcvP4hyhf4fLFgwWhOHQkx6SgtPBKELp6D2qNAfLlvVtNu5Vw5YiLhNljx185TPcUq/gXDW/OHiabucvBCGbbkL8lFi3fXbeA==")
    unsign("R7TCs6Tou2U0otVAzOXQpe1PbcNVUe1MFzDa3GrKsiHAEOzO4YA9knUMf+rA vByA7Q/9er1nhGWIUuvZ7ekhFnG5MfvxrEG9/Y5djqNhSWplAq/Vla5DgQix WPeBQF0EdAzyxeJlGFG2fLCNGUea2w3tuZpTm89stfYCtLNzZqvIe1bJVriR axC9Y1ZzTgz5")
    unsign("R7TCs6Tou2U0otVAzOXQpS2m307PUp7Qr4z2xbvmrQHMHikEDszBZHjtp18s 7mPEWvrc/OQtd5jONADDL4kSfXCJ1Z1ZUFvY9Vjfs5VA3p0qHndKNpD73tYU X/nl7EYF20bjHNiPlD9I2wZrWRZ2pUCVyNLgJ4MqgpFW5kSIPU5cM1TNNR5D 76SADQAnzyvk")
    # b'T\x06\x04\x02\x03SR\x077c7d70b32de1efec100010519c06|7.9.434|720|1280|10000431|9|1|ASUS_I005DA|1736|10000431|4|0|1765027970296|0|d6423cb77c7d70b32de1efec100010519c06|9768b9e4bfcf6c35|||d6423cb77c7d70b32de1efec100010519c06|1\x01'
    # b'T\x06\x04\x02\x03SR\x077c7d70b32de1efec100010519c06|7.9.434|720|1280|10000431|9|1|ASUS_I005DA|1736|10000431|4|0|1765028877450|0|d6423cb77c7d70b32de1efec100010519c06|9768b9e4bfcf6c35|||d6423cb77c7d70b32de1efec100010519c06|1\x01'
    # b'Rv1rPTnczce|1765027969519|0|d6423cb77c7d70b32de1efec100010519c06|1|7.9.434|0|ed63ed85e036078af1d7e3b6347d1b45|f189adc92b816b3e9da29ea304d4a7e4\x02\x02'
    # b'Rv1rPTnczce|1765028876348|0|d6423cb77c7d70b32de1efec100010519c06|1|7.9.434|0|fe883f30961e07c5b2d41e0023881c92|f189adc92b816b3e9da29ea304d4a7e4\x02\x02'

    # post_data_md5: ed63ed85e036078af1d7e3b6347d1b45

    print("\n")
    uninfo("b4nNNPe0FfY7XgDyiz8rayu8FK3ZeUBW1GpBi3VnQHVDDmF81eKT4x9LcvX+2G/j0SYp12TPPh/Tnz5qZnGLEiE7rQ8nMSQOUIRIKPY5Lp2N7vjxPk9Sklh/2nrYz+J86RSfn1Lyzrd8xzTVFHMbHWE8t5ColR7/IkPy6YVBF++q1rWnl2OyM8jxjRNgA7i7rC/nZZkD3s44mFHOXZQ0kZl9H5KmCVQYCrZb6GEr8TCgBqBT+7XI/n1v9HHm8QfCnQxkHdqak0lK6TbJbtqZYw==")
    uninfo("b4nNNPe0FfY7XgDyiz8rayu8FK3ZeUBW1GpBi3VnQHVDDmF81eKT4x9LcvX+2G/j0SYp12TPPh/Tnz5qZnGLEiE7rQ8nMSQOUIRIKPY5Lp2N7vjxPk9Sklh/2nrYz+J86RSfn1LyzreN7ymjGVZM+B47NSDzjHW5Ol9PI6Aha+Z7kwMP0Dz9xvnK+ZdnRlvfkKBvKYuRkcDcdLk9TK+eZmjCWlKQBY9jIX1JhzUnYyrfwdlX42/dFfE2w/Tk5B83rPbo/zr1HlWczT4VnerYEA==")
    unsign("R7TCs6Tou2U0otVAzOXQpYkZEQNQ2rkoLwG0Ooz9JET/eFWSHbfe4PnRNRm1 8iPO/3JMLaa3K21X01sO8zm8q2n8/1FD0EFqPI/p8vNX2x16WUDO+a9RHfQ0 mQm6CrWma3K3id8GnW8Oj2CTnwKRAs9bXcR4NOwPK91IjrHdXTYRKERoXjzC 82W1rudlkXSe")
    ensign("Rv1rPTnczce|1765043634664|0|d6423cb77c7d70b32de1efec100010519c06|1|7.9.434|0|654256a2b780004c3670d5c52b5e78e8|f189adc92b816b3e9da29ea304d4a7e4\x02\x02")