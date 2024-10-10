
湖北理工学院图书馆预约


___爬虫分析___

登录页面：http://zwyd.hbpu.edu.cn


登录页面：http://zwyd.hbpu.edu.cn
输入账号密码，密码被加密，暂未逆向，验证码实际上输入任意值都可以通过
打开F12，开发者工具，随便输入账号，密码，验证码，登录

**爬虫分析**

*1.登录获取tgt与ticket*

```https://cas.hbpu.edu.cn/lyuapServer/v1/tickets```


```
username: 账号
password: 加密的密码
service: http://zwyd.hbpu.edu.cn
loginType: 
id: 
code: 验证码
```

```
{'tgt': 'TGT-132637-7e52b298829xxxxxxxxxxx'0cf6c36d52d', 'ticket': 'ST-132637-b1995xxxxxxxxxxx90bcf652d4ee5'}
```

