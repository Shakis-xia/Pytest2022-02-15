import pytest
import requests
from string import Template
from common8.case import read_excel,get_columns,check,send_requests,save_attach_args_to_dict
module = 'attach'
columns = get_columns(module)
cases = read_excel(f'{module}.xlsx',columns)
s = requests.session()
attach_args_dict = {}
@pytest.mark.parametrize('caseinfo,url,method,type,attach_args,args,expect_res',cases)
def test_login(caseinfo,url,method,type,attach_args,args,expect_res):
    global s,attach_args_dict
    new_data = Template(str(args)).substitute(attach_args_dict)
    print(new_data)
    res_type,real_res,s = send_requests(url,method,type,new_data,s)
    if '01' in caseinfo:
        real_res = {'username':'admin','password':'123456'}
    elif '02' in caseinfo:
        real_res = {'name':'xxk','list':[{'name':'dm'},{'name':'dd'}]}
    else:
        pass
    attach_args_dict = save_attach_args_to_dict(attach_args,real_res,attach_args_dict)
    print(attach_args_dict)
    res_type,real_res,s = send_requests(url,method,type,new_data,s)
    passed,msg = check(caseinfo,expect_res,res_type,real_res)
    assert passed,msg

if __name__ == '__main__':
    import time
    now = time.strftime('%y-%m-%d_%H:%M:%S')
    pytest.main(['--tb=short',f'--html=../report/{module}_{now}.html',f'{module}.py'])