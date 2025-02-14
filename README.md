
湖北理工学院图书馆预约

登录页面：http://zwyd.hbpu.edu.cn

配置文件
```
config = {
    "user": 20224000001,#你的账号
    "pw": "192947401ba2cd9c04331e056d00ee856895f441d5e07fdfac400711cd04c9c3d953f52",#加密的密码
    "seat": "T1-1-005",#座位号
    "StartTime": "07:00:00",#座位开始时间
    "EndTime": "22:00:00",#座位结束始时间
}
```
由于系统22:30开放预约第二天，建议定时22：30运行，默认预约第二天

首次使用需浏览器F12开发者选项，输入账号密码登录，抓取加密密码，验证码输入任意值都可登录
![1728541289515](https://github.com/user-attachments/assets/6123b992-8a0b-416b-bd0b-d8ff2bdf500f)

![1728542073915](https://github.com/user-attachments/assets/236240b2-6d29-4594-86fe-3d43819e3d34)





___爬虫分析___





___1.登录获取tgt与ticket___

**URL**
```
https://cas.hbpu.edu.cn/lyuapServer/v1/tickets
```
```
username: 账号
password: 加密的密码
service: http://zwyd.hbpu.edu.cn
loginType: 
id: 
code: 验证码（未进行验证，任意数值都行）
```

**响应**
```
{'tgt': 'TGT-132637-7e52b298829xxxxxxxxxxx'0cf6c36d52d', 'ticket': 'ST-132637-b1995xxxxxxxxxxx90bcf652d4ee5'}
```




___2. 用ticket获取redirectUrl与extInfo___
**URL**
```
http://zwyd.hbpu.edu.cn/ic-web/auth/address
```

```
'queryParam': f'?ticket={ticket}#/'
```

**响应**
```
{
code: 0,
message: "查询成功",
data: http://zwyd.hbpu.edu.cn/authcenter/toLoginPage?redirectUrl=http%3A%2F%2Fzwyd.hbpu.edu.cn%2Fic-web%2F%2Fauth%2Ftoken%3F%26uuid%3D820686eXXXXXXXXXXXextInfo=P3RpY2tldD1TVC0xNDAzNTXXXXXXXXXNmRiZGQ4MTNlNmIjLw==,
count: 0,
vals: null
}
```
从返回值data中获取redirectUrl 和 extInfo




___3. 重定向到登录页面___
**URL**
```
http://zwyd.hbpu.edu.cn/authcenter/toLoginPage
```

```
{
        'redirectUrl': redirectUrl,
        'extInfo': extInfo,
}
```

**响应**
```

https://cas.hbpu.edu.cn/lyuapServer/login?service=http%3A%2F%2Fzwyd.hbpu.edu.cn%2Fauthcenter%2FdoAuth%2F15b721b54XXXXXXXXXXX
```
从返回值中获取doAuth



___3. 用ticket、doAuth获取uuid、uniToken、extInfo___
**URL**
```
http://zwyd.hbpu.edu.cn/authcenter/doAuth/{do_auth_id}
```

```
{
        'ticket': ticket
    }
```

**响应**
```
http://zwyd.hbpu.edu.cn/ic-web//auth/token?&uuid=820686ed15e841da8c5b9946757ae988&uniToken=eyJhbGciOiJIUzUxMiIsImNhbGciOiJHWklQIn0.H4sIAAAAAAAAAGVQu24CMRD8F9cU3AOR0HINzTXQoRQr7yYx8uNkr6VDKP8eIzjbiMLF7GjGM3MT2v0oO4IhsRPtum3T-2y6dS9Wgn2kB2Oj1ishwePoFqRwn_CCQEoXLReSLA9K7h0WuYYQaj-kiWts4OJ8fQg0vxjmOwPHsCAyoHTOgegpZG76dbYEiIGdGYAhSy2TP12nEoFMLijnY_qnqOe6zLPv8Znk_JXM5kl5wqHShBRFOXvIM6l7NBGt-k5qTBtDxPfhk5PYNdv2Y9M3fdf9_QPp9zsZpgEAAA.0XD-Ct1CJkJIUg40spFiW_G8td7NDW-Y43obNbsaxnuZmkpNs_qQqgazFx5rkII9IeacrolY8xaFHkqgzDMtug&extInfo=P3RpY2tldD1TVC0xNDAzNTItY2IxZDk2OTA1YWIxNDE1ZmE3ZjliNmRiZGQ4MTNlNmIjLw==
```


___4. 获取cookie___
**URL**
```
http://zwyd.hbpu.edu.cn/ic-web//auth/token
```
```
{
            "uuid": uuid,
            "uniToken": uniToken,
            "extInfo": extInfo,
}
```

___5. cookie获取个人信息___
```
http://zwyd.hbpu.edu.cn/ic-web/auth/userInfo
```

___6. cookie进行预约___
```
http://zwyd.hbpu.edu.cn/ic-web/reserve
```
