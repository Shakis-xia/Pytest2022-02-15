--登录接口
--测试成功登录，test01写库、成功登录的姓名写库
delete from info where id=4
delete from users where id=4
insert into users(id, username, password) values(4, 'test01', md5('123456'))
insert into info(id, name) values(4, '成功登录用户')

--测试密码为空，test02写库、登录密码为空写库
delete from info where id=5
delete from users where id=5
insert into users(id, username, password) values(5, 'test02', md5('123456'))
insert into info(id, name) values(5, '登录密码为空')

--测试用户名错误，删test03、姓名登录用户名错误
delete from info where name='登录用户名错误'
delete from users where username='test03'

--测试密码错误，test04写库、姓名登录密码错误写库
delete from info where id=6
delete from users where id=6
insert into users(id, username, password) values(6, 'test04', md5('123456'))
insert into info(id, name) values(6, '登录密码错误')

--测试用户名与密码均错误，删test05、姓名登录用户名与密码均错误
delete from info where name='登录用户名与密码均错误'
delete from users where username='test05'