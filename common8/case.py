from common8.log import log
import requests,pandas,openpyxl
from common8.conf import Conf
def get_columns(module):
    try:
        if module == 'login':
            columns = ['用例编号','用例名称','接口路径','请求方法','请求类型','参数','预期结果']
        elif module == 'signup':
            columns = ['用例编号','用例名称','接口路径','请求方法','请求类型','参数','预期结果','验库sql','预期数据库行数']
        elif module == 'attach':
            columns = ['用例编号','用例名称','接口路径','请求方法','请求类型','获得响应参数','参数','预期结果']
        else:
            pass
        log().info(f'获得列名:{module}====成功')
        return columns
    except BaseException as e:
        log().error(f'获得列名====失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()

def read_excel(excelfile,columns):
    try:
        excelfile = '../excelcases/' + excelfile
        data = pandas.read_excel(excelfile,usecols=columns,engine='openpyxl')
        caseinfo = data['用例编号'] +':' + data['用例名称']
        url = Conf().get_server_info() + data['接口路径']
        data.drop(['用例编号','用例名称','接口路径'],axis=1,inplace=True)
        data.insert(0,'用例信息',caseinfo)
        data.insert(1,'请求地址',url)
        data['参数'] = data['参数'].apply(eval)
        data['预期结果'] = data['预期结果'].apply(eval)
        if '预期数据库行数' in data.columns:
            data['预期数据库行数'] = data['预期数据库行数'].apply(eval)
        cases = data.values.tolist()
        log().info(f'读取excel文件:{excelfile}====成功')
        return cases
    except BaseException as e:
        log().error(f'读取excel文件====失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()

def get_res_values(real_res,locate):
    try:
        locate_list = locate.split('.')
        values = real_res
        for i in locate_list:
            locate_list_child = i.split('[')
            if len(locate_list_child) > 1:
                values = values[locate_list_child[0]][int(locate_list_child[1].strip(']'))]
            else:
                values = values[locate_list_child[0]]
        log().info(f'获得响应结果中的对应参数值====成功')
        return values
    except BaseException as e:
        log().error(f'获得响应结果中的对应参数值====失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()

def save_attach_args_to_dict(attach_args,real_res,attach_args_dict):
    try:
        if attach_args == 'None':
            log().info(f'无可存入公共字典的信息,字典：{attach_args_dict}')
            pass
        else:
            list = attach_args.split('|')
            for i in list:
                key = i.split('#')[1]
                values = get_res_values(real_res,i.split('#')[0])
                attach_args_dict[key] = values
            log().info(f'存入公共字典,字典：{attach_args_dict}====成功')
        return attach_args_dict
    except BaseException as e:
        log().error(f'存入公共字典====失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()

def send_requests(url,method,type,args,s=None):
    try:
        if s == None:
            s = requests.session()
        send = f"s.{method}('{url}',{type}={args})"
        res = eval(send)
        if 'text' in res.headers['content-type']:
            res_type = 'text'
            real_res = res.text
        elif 'json' in res.headers['content-type']:
            res_type = 'json'
            real_res = res.json()
        else:
            pass
        log().info('发送请求====成功')
        return res_type,real_res,s
    except BaseException as e:
        log().error(f'发送请求====失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()

def check(caseinfo,expect_res,res_type,real_res):
    try:
        passed = False
        if res_type == 'text' and expect_res in real_res :
            passed = True
        elif res_type == 'json' and expect_res == real_res :
            passed = True
        else:
            pass
        if passed:
            msg=''
            log().info(f'{caseinfo}====响应结果比对====成功!')
        else:
            msg = f'{caseinfo}====响应结果比对====失败!====expect:{expect_res}====real:{real_res}'
            log().warning(msg)
        return passed,msg
    except BaseException as e:
        log().error(f'响应结果比对====失败，失败类型：{type(e).__name__},失败内容：{e}')
        exit()