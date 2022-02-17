import sys
sys.path.append('..')
import pytest
import requests
from common8.db import DB
from common8.case01 import get_columns,read_excel,send_requests,check,save_args_to_dict
from string import Template
DB().init_db('signup.sql')
module = 'attach'
columns = get_columns(module)
cases = read_excel(f'{module}.xlsx',columns)
s = requests.session()
attach_args_dict = {}
@pytest.mark.parametrize('caseinfo,url,method,type,attach_args,args,first_do,expect_res',cases)
def test_attach(caseinfo,url,method,type,attach_args,args,first_do,expect_res):
    global s,attach_args_dict
    new_data = Template(str(args)).substitute(attach_args_dict)
    if "重置s" in first_do:
        s = None
    res_type, real_res, s = send_requests(caseinfo, url, method, type, new_data, s)
    if '01' in caseinfo:
        real_res = {'username': 'admin', 'password': '123456'}
    elif '02' in caseinfo:
        real_res = {'name': 'xxk', 'list': [{'name': 'dm'}, {'name': 'dd'}]}
    else:
        pass

    attach_args_dict = save_args_to_dict(attach_args,real_res,attach_args_dict)
    res_type,real_res,s = send_requests(caseinfo,url,method,type,new_data,s)
    passed,msg = check(caseinfo,res_type,real_res,expect_res)
    assert passed,msg

if __name__ == '__main__':
    import time
    now = time.strftime('%y-%m-%d_%H:%M:%S')
    pytest.main(['--tb=short',f'--html=../report/{module}_{now}.html',f'{module}01.py'])