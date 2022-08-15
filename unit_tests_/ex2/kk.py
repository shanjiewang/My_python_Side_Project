# pytest --cov kk   # 顯示報告
# pytest --cov-report term-missing --cov=kk
# pytest -v --html=./outputs/kk_report.html 生成 html 報告

def aa(x,y):
    z=x+y
    return z

def bb(x,y):
    z=x*y
    return z

def cc(x,y):
    if type(x)==int and type(y)==int:
        z=x+y
        return z
    else:
        return 0
