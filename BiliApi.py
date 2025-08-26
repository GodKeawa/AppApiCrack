import requests
import hashlib
import time
import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from os import urandom
from urllib.parse import urlencode
import base64

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
}

hash_key_api = "http://passport.bilibili.com/x/passport-login/web/key?"
hash_key_infos = "appkey=783bbb7264451d82&build=7470300&buvid=XZC1AF7C636867FDB17CB167546A1374EE09E&c_locale=zh_CN&channel=bili&disable_rcmd=0&local_id=XZC1AF7C636867FDB17CB167546A1374EE09E&mobi_app=android&platform=android&s_locale=zh_CN&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%227.47.0%22%2C%22abtest%22%3A%22%22%7D"

login_api = "https://passport.bilibili.com/x/passport-login/oauth2/login"
login_dict = {
    'appkey': '783bbb7264451d82',
    "bili_local_id": "baa587c2f0fb3c209395966d61a8b70620250825205028c45430422f0162cfd5",
    "build":"7470300",
    "buvid" : "XZC1AF7C636867FDB17CB167546A1374EE09E",
    "c_locale" : "zh_CN",
    "channel" : "bili" ,
    "device" : "phone",
    'device_meta': None,
    'disable_rcmd': '0',
    'dt': None,
    'local_id': 'XZC1AF7C636867FDB17CB167546A1374EE09E',
    'mobi_app': 'android',
    'password': None,
    'platform': 'android',
    's_locale': 'zh_CN',
    "statistics" : "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%227.47.0%22%2C%22abtest%22%3A%22%22%7D",
    'ts': None,
    'username': None,
}
# example
device_meta_raw = """{
    "aaid": "",
    "accessibility_service": "[\"com.android.settings/.accessibility.accessibilitymenu.AccessibilityMenuService\", \"com.google.android.marvin.talkback/.TalkBackService\", \"com.google.android.marvin.talkback/com.google.android.accessibility.accessibilitymenu.AccessibilityMenuService\", \"com.google.android.marvin.talkback/com.google.android.accessibility.selecttospeak.SelectToSpeakService\", \"com.google.android.marvin.talkback/com.android.switchaccess.SwitchAccessService\", \"com.miui.accessibility/.voiceaccess.VoiceAccessAccessibilityService\", \"com.miui.accessibility/.haptic.HapticAccessibilityService\", \"com.miui.personalassistant/com.miui.voicesdk.VoiceAccessibilityService\", \"com.miui.securitycenter/com.miui.gamebooster.gbservices.AntiMsgAccessibilityService\", \"com.miui.securitycenter/com.miui.luckymoney.service.LuckyMoneyAccessibilityService\", \"com.miui.voiceassist/com.miui.voicesdk.VoiceAccessibilityService\", \"com.xiaomi.gamecenter.sdk.service/com.xiaomi.gamecenter.sdk.ui.mifloat.process.DetectService\", \"com.xiaomi.misettings/.usagestats.focusmode.service.LRAccessibilityService\", \"bin.mt.plus/bin.mt.function.ar.ActivityRecordService\", \"com.baidu.searchbox/.push.PushAccessibilityService\", \"com.ss.android.ugc.aweme/.live.livehostimpl.AudioAccessibilityService\"]",
    "adb_enabled": "0",
    "adid": "ddad409099a5ad09",
    "androidapp20": "[\"480000,com.miui.screenrecorder,0,1.9.4,94,480000\", \"1721481064873,icu.nullptr.applistdetector,0,2.3,43,1721481064873\", \"1721481071513,com.tsng.applistdetector,0,1.3.2,11,1721481071513\", \"1724609783795,com.tencent.mm,0,8.0.50,2701,1724609783795\", \"478000,com.xiaomi.mibrain.speech,0,1.1.5,15,478000\", \"479000,com.miui.huanji,0,3.1.5,30015,479000\", \"1724684106215,com.baidu.searchbox,0,13.64.0.10,444597504,1724684106215\", \"1721630422319,com.xmcy.hykb,0,1.5.7.506,341,1721630422319\", \"1721480199568,bin.mt.plus,0,2.16.3,24071712,1721480199568\", \"478000,com.miui.virtualsim,0,5.9.2,592,478000\", \"479000,com.miui.compass,0,9.5.5,62,479000\", \"1730015839618,com.xunmeng.pinduoduo,0,7.31.0,73100,1730015839618\", \"1745575540286,com.bilibili.app.in,0,3.15.0,7040200,1745575540286\", \"1733679005370,com.ecom.renrentong,0,1.1.9,119,1733679005370\", \"479000,com.xiaomi.shop,0,5.0.4.20191224.r4,20191224,479000\", \"1734597791657,com.ss.android.ugc.aweme,0,32.6.0,320601,1734597791657\", \"1721480745088,io.github.huskydg.magisk,0,26.4-kitsune,26400,1721480745088\", \"1721629305812,com.tencent.mobileqq,0,9.0.75,6808,1721629305812\", \"1722163631783,com.pwrd.steam.esports,0,3.4.0.157,157,1722163631783\", \"479000,com.miui.notes,0,3.2.2,322,479000\"]",
    "androidappcnt": 304,
    "androidsysapp20": "[\"1230768000000,com.android.cts.priv.ctsshim,1,9-5374186,28,1230768000000\", \"1230768000000,com.miui.contentextension,1,2.4.2,10164,1230768000000\", \"1230768000000,com.qualcomm.qti.qcolor,1,10,29,1230768000000\", \"1230768000000,com.android.internal.display.cutout.emulation.corner,1,1.0,1,1230768000000\", \"1230768000000,com.qualcomm.qti.improvetouch.service,1,10,29,1230768000000\", \"1230768000000,com.android.internal.display.cutout.emulation.double,1,1.0,1,1230768000000\", \"1230768000000,com.android.providers.telephony,1,10,29,1230768000000\", \"1230768000000,com.android.dynsystem,1,10,29,1230768000000\", \"1230768000000,com.miui.powerkeeper,1,4.2.00,40200,1230768000000\", \"1230768000000,com.goodix.fingerprint,1,1.0.04,4,1230768000000\", \"1230768000000,com.xiaomi.miplay_client,1,0.4.32,132,1230768000000\", \"1230768000000,com.unionpay.tsmservice.mi,1,01.00.26,27,1230768000000\", \"1230768000000,com.android.providers.calendar,1,10.0.4.5,10000405,1230768000000\", \"1230768000000,com.miui.contentcatcher,1,1.0.001,1,1230768000000\", \"1230768000000,com.android.providers.media,1,10,1023,1230768000000\", \"1230768000000,com.milink.service,1,12.4.1.2,12040102,1230768000000\", \"1230768000000,com.qti.service.colorservice,1,1.0,1,1230768000000\", \"1230768000000,com.android.theme.icon.square,1,1.0,1,1230768000000\", \"1230768000000,com.android.internal.systemui.navbar.gestural_wide_back,1,1.0,1,1230768000000\", \"1230768000000,com.xiaomi.powerchecker,1,2.0.00,20000,1230768000000\"]",
    "app_id": "14",
    "app_version": "3.15.0",
    "app_version_code": "7040200",
    "apps": "[\"480000,com.miui.screenrecorder,0,1.9.4,94,480000\",\"1721481064873,icu.nullptr.applistdetector,0,2.3,43,1721481064873\",\"1230768000000,com.android.cts.priv.ctsshim,1,9-5374186,28,1230768000000\",\"1230768000000,com.miui.contentextension,1,2.4.2,10164,1230768000000\",\"1230768000000,com.qualcomm.qti.qcolor,1,10,29,1230768000000\",\"1230768000000,com.android.internal.display.cutout.emulation.corner,1,1.0,1,1230768000000\",\"1230768000000,com.qualcomm.qti.improvetouch.service,1,10,29,1230768000000\",\"1230768000000,com.android.internal.display.cutout.emulation.double,1,1.0,1,1230768000000\",\"1230768000000,com.android.providers.telephony,1,10,29,1230768000000\",\"1230768000000,com.android.dynsystem,1,10,29,1230768000000\",\"1230768000000,com.miui.powerkeeper,1,4.2.00,40200,1230768000000\",\"1230768000000,com.goodix.fingerprint,1,1.0.04,4,1230768000000\",\"1230768000000,com.xiaomi.miplay_client,1,0.4.32,132,1230768000000\",\"1230768000000,com.unionpay.tsmservice.mi,1,01.00.26,27,1230768000000\",\"1230768000000,com.android.providers.calendar,1,10.0.4.5,10000405,1230768000000\",\"1230768000000,com.miui.contentcatcher,1,1.0.001,1,1230768000000\",\"1230768000000,com.android.providers.media,1,10,1023,1230768000000\",\"1230768000000,com.milink.service,1,12.4.1.2,12040102,1230768000000\",\"1230768000000,com.qti.service.colorservice,1,1.0,1,1230768000000\",\"1230768000000,com.android.theme.icon.square,1,1.0,1,1230768000000\"]",
    "axposed": "false",
    "band": "4.0.c2.6-00335-0220_1946_40a1464,4.0.c2.6-00335-0220_1946_40a1464",
    "battery": 10,
    "batteryState": "BATTERY_STATUS_CHARGING",
    "battery_health": "2",
    "battery_plugged": "1",
    "battery_present": "true",
    "battery_technology": "Li-poly",
    "battery_temperature": "370",
    "battery_voltage": "3960",
    "biometric": "1",
    "biometrics": "touchid",
    "boot": "665894",
    "brand": "Xiaomi",
    "brightness": "133",
    "bssid": "80:12:df:ac:6e:4e",
    "btmac": "",
    "build_id": "QKQ1.190828.002 test-keys",
    "buvid_local": "XUE2463E4562DA33E243BB6DDFB4C74286237",
    "cell": "{\"lac\":\"31010\",\"cid\":\"56343\",\"type\":\"gsm\"}",
    "chid": "master",
    "countryIso": "",
    "cpuCount": "8",
    "cpuFreq": "1766400",
    "cpuModel": "",
    "cpuVendor": "Qualcomm",
    "data_activity_state": "0",
    "data_connect_state": "0",
    "data_network_type": "0",
    "device_angle": "-0.6267704,-0.3418613,-0.2813414",
    "drmid": "2693071d940787d5b18efa5441cf93d1",
    "emu": "000",
    "files": "/data/user/0/com.bilibili.app.in/files",
    "first": "false",
    "free_memory": "1868759040",
    "fstorage": 44705300480,
    "fts": "1745575576",
    "gadid": "",
    "glimit": "",
    "gps_sensor": "1",
    "guest_id": "24561344813427",
    "guid": "153f5ad7-9528-4141-9bfa-14991bbd3724",
    "gyroscope_sensor": "1",
    "iccid": "",
    "imei": "",
    "imsi": "",
    "is_root": "false",
    "kernel_version": "4.9.186-perf-g10af704",
    "languages": "zh",
    "last_dump_ts": "1745575922908",
    "light_intensity": "20.0",
    "linear_speed_sensor": "1",
    "mac": "A4:50:46:FF:54:49",
    "maps": "",
    "mem": "5903380480",
    "memory": "5903380480",
    "mid": "",
    "model": "MI 8",
    "net": "[\"dummy0,fe80::2c79:dcff:fee9:d7c8%dummy0,2e:79:dc:e9:d7:c8\", \"lo,::1,127.0.0.1,\", \"wlan0,fe80::a650:46ff:feff:5449%wlan0,192.168.2.190,a4:50:46:ff:54:49\", \"rmnet_data0,fe80::cadf:4bd0:446b:5a50%rmnet_data0,\", \"tun0,fe80::e869:8061:ceab:853%tun0,10.1.10.1,\", \"rmnet_ipa0,,\"]",
    "network": "OFFLINE",
    "oaid": "",
    "oid": "",
    "os": "android",
    "osver": "10",
    "proc": "com.bilibili.app.in",
    "props": {
        "gsm.network.type": "Unknown,Unknown",
        "gsm.sim.state": "ABSENT,ABSENT",
        "http.agent": "",
        "http.proxy": "",
        "net.dns1": "",
        "net.eth0.gw": "",
        "net.gprs.local-ip": "",
        "net.hostname": "MI8-MI8",
        "persist.sys.country": "",
        "persist.sys.language": "",
        "ro.boot.hardware": "qcom",
        "ro.boot.serialno": "",
        "ro.build.date.utc": "1635404500",
        "ro.build.tags": "release-keys",
        "ro.debuggable": "0",
        "ro.product.device": "dipper",
        "ro.serialno": "",
        "sys.usb.state": "mtp"
    },
    "rc_app_code": "0000000000",
    "root": False,
    "screen": "1080,2029,440",
    "sdkver": "0.2.4",
    "sensor": "[\"NonUi  Wakeup,XiaoMi\", \"NonUi  Non-wakeup,XiaoMi\", \"tmd2725 Proximity Sensor Wakeup,ams AG\", \"tmd2725 Proximity Sensor Non-wakeup,ams AG\", \"pedometer  Wakeup,qualcomm\", \"pedometer  Non-wakeup,qualcomm\", \"stationary_detect_wakeup,qualcomm\", \"stationary_detect,qualcomm\", \"bosch_bmp285 Pressure Sensor Non-wakeup,Bosch\", \"Game Rotation Vector  Non-wakeup,qualcomm\", \"har_wakeup,xiaomi\", \"har,xiaomi\", \"sns_tilt  Wakeup,qualcomm\", \"sns_smd  Wakeup,qualcomm\", \"Aod  Wakeup,XiaoMi\", \"Aod  Non-wakeup,XiaoMi\", \"device_orient  Wakeup,xiaomi\", \"device_orient  Non-wakeup,xiaomi\", \"ak0991x Magnetometer-Uncalibrated Non-wakeup,akm\", \"gravity  Non-wakeup,qualcomm\", \"sns_geomag_rv  Non-wakeup,qualcomm\", \"tmd2725  Non-wakeup,ams AG\", \"tmd2725 Ambient Light Sensor Wakeup,ams AG\", \"tmd2725 Ambient Light Sensor Non-wakeup,ams AG\", \"pickup  Wakeup,XiaoMi\", \"pickup  Non-wakeup,XiaoMi\", \"tmd2725  Non-wakeup,ams AG\", \"orientation  Non-wakeup,xiaomi\", \"pedometer  Wakeup,qualcomm\", \"pedometer  Non-wakeup,qualcomm\", \"ICM20690,qualcomm\", \"ICM20690,qualcomm\", \"ICM20690,qualcomm\", \"rotation vector  Non-wakeup,xiaomi\", \"linear_acceleration,qualcomm\", \"ak0991x Magnetometer Non-wakeup,akm\", \"ICM20690,qualcomm\", \"motion_detect_wakeup,qualcomm\", \"motion_detect,qualcomm\"]",
    "sensors_info": "[{\"name\":\"NonUi  Wakeup\",\"vendor\":\"XiaoMi\",\"version\":\"1\",\"type\":\"33171027\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"NonUi  Non-wakeup\",\"vendor\":\"XiaoMi\",\"version\":\"1\",\"type\":\"33171027\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"tmd2725 Proximity Sensor Wakeup\",\"vendor\":\"ams AG\",\"version\":\"256\",\"type\":\"8\",\"maxRange\":\"5.0\",\"resolution\":\"0.01\",\"power\":\"1.0\",\"minDelay\":\"0\"}, {\"name\":\"tmd2725 Proximity Sensor Non-wakeup\",\"vendor\":\"ams AG\",\"version\":\"256\",\"type\":\"8\",\"maxRange\":\"5.0\",\"resolution\":\"0.01\",\"power\":\"1.0\",\"minDelay\":\"0\"}, {\"name\":\"pedometer  Wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"19\",\"maxRange\":\"4.2949673E9\",\"resolution\":\"1.0\",\"power\":\"0.15\",\"minDelay\":\"0\"}, {\"name\":\"pedometer  Non-wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"19\",\"maxRange\":\"4.2949673E9\",\"resolution\":\"1.0\",\"power\":\"0.15\",\"minDelay\":\"0\"}, {\"name\":\"stationary_detect_wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"29\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.025\",\"minDelay\":\"-1\"}, {\"name\":\"stationary_detect\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"29\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.025\",\"minDelay\":\"-1\"}, {\"name\":\"bosch_bmp285 Pressure Sensor Non-wakeup\",\"vendor\":\"Bosch\",\"version\":\"8728\",\"type\":\"6\",\"maxRange\":\"1100.0\",\"resolution\":\"0.01\",\"power\":\"0.72\",\"minDelay\":\"40000\"}, {\"name\":\"Game Rotation Vector  Non-wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"15\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.515\",\"minDelay\":\"5000\"}, {\"name\":\"har_wakeup\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"33171070\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"har\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"33171070\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"sns_tilt  Wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"22\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.025\",\"minDelay\":\"0\"}, {\"name\":\"sns_smd  Wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"17\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.025\",\"minDelay\":\"-1\"}, {\"name\":\"Aod  Wakeup\",\"vendor\":\"XiaoMi\",\"version\":\"1\",\"type\":\"33171029\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"Aod  Non-wakeup\",\"vendor\":\"XiaoMi\",\"version\":\"1\",\"type\":\"33171029\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"device_orient  Wakeup\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"27\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"device_orient  Non-wakeup\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"27\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"ak0991x Magnetometer-Uncalibrated Non-wakeup\",\"vendor\":\"akm\",\"version\":\"10058\",\"type\":\"14\",\"maxRange\":\"4912.0\",\"resolution\":\"0.15\",\"power\":\"1.1\",\"minDelay\":\"10000\"}, {\"name\":\"gravity  Non-wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"9\",\"maxRange\":\"156.99008\",\"resolution\":\"0.01\",\"power\":\"0.515\",\"minDelay\":\"5000\"}, {\"name\":\"sns_geomag_rv  Non-wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"20\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"1.05\",\"minDelay\":\"10000\"}, {\"name\":\"tmd2725  Non-wakeup\",\"vendor\":\"ams AG\",\"version\":\"256\",\"type\":\"33171007\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.08\",\"minDelay\":\"10000\"}, {\"name\":\"tmd2725 Ambient Light Sensor Wakeup\",\"vendor\":\"ams AG\",\"version\":\"256\",\"type\":\"5\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.08\",\"minDelay\":\"0\"}, {\"name\":\"tmd2725 Ambient Light Sensor Non-wakeup\",\"vendor\":\"ams AG\",\"version\":\"256\",\"type\":\"5\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.08\",\"minDelay\":\"0\"}, {\"name\":\"pickup  Wakeup\",\"vendor\":\"XiaoMi\",\"version\":\"1\",\"type\":\"33171036\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"pickup  Non-wakeup\",\"vendor\":\"XiaoMi\",\"version\":\"1\",\"type\":\"33171036\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"tmd2725  Non-wakeup\",\"vendor\":\"ams AG\",\"version\":\"256\",\"type\":\"33171005\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"1.0\",\"minDelay\":\"10000\"}, {\"name\":\"orientation  Non-wakeup\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"3\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"pedometer  Wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"18\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.15\",\"minDelay\":\"0\"}, {\"name\":\"pedometer  Non-wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"18\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.15\",\"minDelay\":\"0\"}, {\"name\":\"ICM20690\",\"vendor\":\"qualcomm\",\"version\":\"257\",\"type\":\"16\",\"maxRange\":\"17.452778\",\"resolution\":\"5.3265877E-4\",\"power\":\"2.9\",\"minDelay\":\"2500\"}, {\"name\":\"ICM20690\",\"vendor\":\"qualcomm\",\"version\":\"257\",\"type\":\"4\",\"maxRange\":\"17.452778\",\"resolution\":\"5.3265877E-4\",\"power\":\"2.9\",\"minDelay\":\"2500\"}, {\"name\":\"ICM20690\",\"vendor\":\"qualcomm\",\"version\":\"257\",\"type\":\"1\",\"maxRange\":\"78.4532\",\"resolution\":\"0.0023938033\",\"power\":\"0.44\",\"minDelay\":\"2500\"}, {\"name\":\"rotation vector  Non-wakeup\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"11\",\"maxRange\":\"1.0\",\"resolution\":\"0.01\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"linear_acceleration\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"10\",\"maxRange\":\"156.99008\",\"resolution\":\"0.01\",\"power\":\"0.515\",\"minDelay\":\"5000\"}, {\"name\":\"ak0991x Magnetometer Non-wakeup\",\"vendor\":\"akm\",\"version\":\"10058\",\"type\":\"2\",\"maxRange\":\"4912.0\",\"resolution\":\"0.15\",\"power\":\"1.1\",\"minDelay\":\"10000\"}, {\"name\":\"ICM20690\",\"vendor\":\"qualcomm\",\"version\":\"257\",\"type\":\"35\",\"maxRange\":\"78.4532\",\"resolution\":\"0.0023938033\",\"power\":\"0.44\",\"minDelay\":\"2500\"}, {\"name\":\"motion_detect_wakeup\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"30\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.025\",\"minDelay\":\"-1\"}, {\"name\":\"motion_detect\",\"vendor\":\"qualcomm\",\"version\":\"1\",\"type\":\"30\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.025\",\"minDelay\":\"-1\"}]",
    "sim": "1",
    "speed_sensor": "1",
    "ssid": "\"ChinaNet-VFzE-5G\"",
    "str_app_id": "14",
    "str_battery": "10",
    "str_brightness": "133",
    "sys": {
        "cpu_abi": "arm64-v8a",
        "cpu_abi2": "",
        "cpu_abi_libc": "ARM",
        "cpu_abi_libc64": "ARM64",
        "cpu_abi_list": "arm64-v8a,armeabi-v7a,armeabi",
        "cpu_features": "fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp",
        "cpu_hardware": "Qualcomm Technologies, Inc SDM845",
        "cpu_model_name": "",
        "cpu_processor": "AArch64 Processor rev 12 (aarch64)",
        "device": "dipper",
        "display": "QKQ1.190828.002 test-keys",
        "fingerprint": "Xiaomi/dipper/dipper:10/QKQ1.190828.002/V12.5.2.0.QEACNXN:user/release-keys",
        "hardware": "qcom",
        "manufacturer": "Xiaomi",
        "product": "dipper",
        "serial": "unknown"
    },
    "systemvolume": 0,
    "t": "1745575991197",
    "totalSpace": 56283402240,
    "udid": "ddad409099a5ad09",
    "ui_version": "V12.5.2.0.QEACNXN",
    "uid": "10202",
    "usb_connected": "1",
    "vaid": "",
    "virtual": "0",
    "virtualproc": "[]",
    "voice_network_type": "0",
    "wifimac": "A4:50:46:FF:54:49",
    "wifimaclist": [
        {
            "bssid": "80:12:df:ac:6e:4d",
            "ssid": "ChinaNet-VFzE"
        },
        {
            "bssid": "80:12:df:ac:6e:4e",
            "ssid": "ChinaNet-VFzE-5G"
        },
        {
            "bssid": "00:4f:1a:59:cd:ac",
            "ssid": "ChinaNet-401"
        }
    ]
}"""

login_secret = "2653583c8873dea268ab9386918b1d65"

api = "https://app.biliapi.net/x/v2/space?"
# 私钥
access_key= "access_key"
ad_extra = "not necessary"
# 公共参数
infos = "appkey=1d8b6e7d45233436&build=7470300&c_locale=zh_CN&channel=bili&disable_rcmd=0&fnval=272&fnver=0&force_host=0&fourk=0&from=0&local_time=8&mobi_app=android&platform=android&player_net=1&qn=32&s_locale=zh_CN&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%227.47.0%22%2C%22abtest%22%3A%22%22%7D"

secretkey = "560c52ccd288fed045859ed18bffd973"

# 生成请求参数
def get_request(uid: int) -> str:
    request = ""
    request += "access_key=" + access_key
    request += "&ad_extra=" + ad_extra
    request += "&" + infos
    request += "&ts=" + str(int(time.time()))
    request += "&vmid=" + str(uid)

    sign = hashlib.md5((request+secretkey).encode("utf-8")).hexdigest()
    print("sign: ", sign)
    request += "&sign=" + sign
    return request

def get_access_key(username: str, password: str) -> str:
    # prepare device_meta and dt
    aes_key = urandom(16)
    aes_iv = aes_key
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(device_meta_raw.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    device_meta = base64.b64encode(ciphertext).decode('utf-8')

    # get hash and key
    timestamp = "&ts=" + str(int(time.time()))
    sign = hashlib.md5((hash_key_infos + timestamp + login_secret).encode("utf-8")).hexdigest()
    print("sign: ", sign)
    request = hash_key_api + hash_key_infos + timestamp + "&sign=" + sign
    response = requests.get(headers=headers, url=request)
    data = response.json()
    hash = data["data"]["hash"]
    key = data["data"]["key"]
    print("hash: ", hash)
    print("key: ", key)
    # encrypt password and aes key
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode("utf-8"))
    hash_password = rsa.encrypt((hash + password).encode(), pubkey)
    hash_password = base64.b64encode(hash_password).decode("utf-8")
    print("hash_password: ", hash_password)
    dt = rsa.encrypt(str(aes_key).encode(), pubkey)
    dt = base64.b64encode(dt).decode("utf-8")

    login_dic = login_dict.copy()
    login_dic["device_meta"] = device_meta
    login_dic["ts"] = str(int(time.time()))
    login_dic["dt"] = dt
    login_dic["password"] = hash_password
    login_dic["username"] = username
    login_str = urlencode(login_dic)
    sign = hashlib.md5((login_str + login_secret).encode("utf-8")).hexdigest()
    login_dic.update({"sign": sign})
    body = urlencode(login_dic)
    print("body: ", body)
    response = requests.post(headers=headers, url=login_api, data=login_dic)
    data = response.json()
    print("data: ", data)
    return data["data"]["token_info"]["access_token"]


if __name__ == '__main__':
    get_access_key("username", "password")
    # uid = 8427588
    # request = get_request(uid)
    # url = api + request
    # print("url: ", url)
    # response = requests.get(url)
    # print("response: ", response.json())