import pymysql
import sys
sys.path.append('..')
from common8.log import log
from common8.conf import Conf
def read_sqls(sqlsfile):
    try:
        sqlsfile = '../initsqls/' + sqlsfile
        data = open(sqlsfile,'r',encoding='utf-8')
        sqls = []
        for sql in data:
            if sql.strip() and sql[:2] != '--':
                sqls.append(sql.strip())
        log().info(f'{sqlsfile}读取成功')
        return sqls
    except BaseException as e:
        log().error(f'{sqlsfile}读取失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()

class DB:
    def __init__(self):
        try:
            self.__conn = pymysql.connect(**Conf().get_db_info())
            self.__yb = self.__conn.cursor()
            log().info(f'连接数据库====成功')
        except BaseException as e:
            log().error(f'连接数据库====失败，失败类型：{type(e).__name__},失败内容：{e}')
            exit()
    def init_db(self,sqlsfile):
        try:
            sqls = read_sqls(sqlsfile)
            for sql in sqls:
                self.__yb.execute(sql)
            self.__conn.commit()
            self.__conn.close()
            log().info(f'初始化数据库====成功')
        except BaseException as e:
            log().error(f'初始化数据库====失败，失败类型：{type(e).__name__},失败内容：{e}')
            exit()
    def check_db(self,caseinfo,check_sql,exptce_db_res):
        try:
            self.__yb.execute(check_sql)
            real_db_res = self.__yb.fetchone()
            passed = False
            if exptce_db_res == real_db_res:
                passed = True
            if passed:
                log().info(f'验证数据库====成功')
                msg = ''
            else:
                msg = f'{caseinfo}:验证数据库====失败，期望：{exptce_db_res}；实际：{real_db_res}'
                log().warning(msg)
            return passed,msg
        except BaseException as e:
            log().error(f'验证数据库====失败，失败类型：{type(e).__name__},失败内容：{e}')
            exit()