# AppApiCrack
为了某些工作进行的AppApi签名破解研究
本项目并不提供完整的api调用框架, 仅展示App的接口签名的加密机制

## Bibibili
提供一个基本的api调用示例
对于不同平台(对应app_key)的secret_key可以参考https://blog.kaaass.net/archives/947
同时提供示例device_meta, 结构可以参考, 但不同的设备信息会影响风控，建议抓包获取access_key后再访问其他接口
接口的签名加密机制参考示例

登录接口目前受到风控影响基本无法正常使用, 需要手动处理验证码请求
当账号登录被风控时, 会返回一个验证码的url, 需要手动打开浏览器访问该url, 完成验证后再次调用登录接口即可
但注意浏览器需要配置环境, 否则验证码无法刷新出来

目前提供了获取用户主页信息的示例接口, 只需要通过抓包获取access_key即可, 通常会附带一个ad_extra
B站app的主页接口在未登录时只会返回部分信息, 需要登录后才能获取完整信息, 比如IP地址等

## Qidian 起点中文网
提供QdSign和Qd_info签名的解析加密示例
因为起点可以不登录使用，故尚未破解登录接口
`crypto.py`中提供了QdSign和Qd_info的解析函数，使用unsign和uninfo解析出明文，使用ensign和eninfo进行签名

## Environment
使用python的uv构建环境, 或者安装pyproject.toml中的依赖

