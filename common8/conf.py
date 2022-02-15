import configparser
from common8.log import log
class Conf():
    def __init__(self):
        try:
            self.__conf = configparser.ConfigParser()
            self.__conf.read('../conf/entry.ini',encoding='utf-8')
            self.__server = self.__conf.get('entry','server')
            self.__db = self.__conf.get('entry','db')
            log().info(f'获取入口成功，服务器：{self.__server}；数据库：{self.__db}')
        except BaseException as e:
            log().error(f'获取入口失败，失败类型：{type(e).__name__},失败内容：{e}')
            exit()
    def get_server_info(self):
        try:
            self.__conf.read('../conf/server.conf',encoding='utf-8')
            ip = self.__conf.get(self.__server,'ip')
            port = self.__conf.get(self.__server,'port')
            host = f'http://{ip}:{port}'
            log().info(f'获取服务器信息成功:{host}')
            return host
        except BaseException as e:
            log().error(f'获取服务器信息失败，失败类型：{type(e).__name__},失败内容：{e}')
            exit()
    def get_db_info(self):
        try:
            self.__conf.read('../conf/db.conf', encoding='utf-8')
            host = self.__conf.get(self.__db, 'host')
            user = self.__conf.get(self.__db, 'user')
            passwd = self.__conf.get(self.__db, 'passwd')
            db = self.__conf.get(self.__db, 'db')
            db_info = {'host':host,"user":user,'passwd':passwd,'db':db}
            log().info(f'获取数据库信息成功:{db_info}')
            return db_info
        except BaseException as e:
            log().error(f'获取数据库信息失败，失败类型：{type(e).__name__},失败内容：{e}')
            exit()