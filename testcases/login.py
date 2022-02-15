import pytest
from common8.db import DB
from common8.case import read_excel,get_columns,check,send_requests
module = 'login'
DB().init_db(f'{module}.sql')
columns = get_columns(module)
cases = read_excel(f'{module}.xlsx',columns)
@pytest.mark.parametrize('caseinfo,url,method,type,args,expect_res',cases)
def test_login(caseinfo,url,method,type,args,expect_res):
    res_type,real_res,s = send_requests(url,method,type,args)
    passed,msg = check(caseinfo,expect_res,res_type,real_res)
    assert passed,msg

if __name__ == '__main__':
    import time
    now = time.strftime('%y-%m-%d_%H:%M:%S')
    pytest.main(['--tb=short',f'--html=../report/{module}_{now}.html',f'{module}.py'])