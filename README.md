
湖北理工学院图书馆预约


___爬虫分析___

登录页面：http://zwyd.hbpu.edu.cn


**爬虫分析**

1.登录获取tgt与ticket

**URL**
```
https://cas.hbpu.edu.cn/lyuapServer/v1/tickets
```

**请求头**
```
username: 账号
password: 加密的密码
service: http://zwyd.hbpu.edu.cn
loginType: 
id: 
code: 验证码
```

**响应**
```
{'tgt': 'TGT-132637-7e52b298829xxxxxxxxxxx'0cf6c36d52d', 'ticket': 'ST-132637-b1995xxxxxxxxxxx90bcf652d4ee5'}
```

2. 用ticket获取新的定向网址
