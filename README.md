
湖北理工学院图书馆预约

**爬虫分析**

登录页面：http://zwyd.hbpu.edu.cn
![1728538356970](https://github.com/user-attachments/assets/a9c21662-d7dd-4b5b-958e-497dd2b6ba43)



登录页面：http://zwyd.hbpu.edu.cn
输入账号密码，密码被加密，暂未逆向，验证码实际上输入任意值都可以通过
打开F12，开发者工具，随便输入账号，密码，验证码，登录

找到
https://cas.hbpu.edu.cn/lyuapServer/v1/tickets这个请求，里面请求头为

username:	123
password:	12a5d0523e124
service:	http://zwyd.hbpu.edu.cn
loginType:	
id:	ed5fb1132ffa45a2a97f3780167a648f
code:	1
