import os

import pytest

if __name__ == '__main__':
    # allure结果会累加,所以用clean清除history
    os.system('rd /s/q temp')
    os.system('rd /s/q report')

    pytest.main(['-s', 'test_web.py', '--alluredir', './temp'])
    os.system('allure generate ./temp -o ./report --clean')
