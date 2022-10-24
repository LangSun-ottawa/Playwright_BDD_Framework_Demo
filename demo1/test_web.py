import allure
import pytest
import yaml
from playwright.sync_api import sync_playwright

f = open('testcase.yaml', mode='r', encoding='utf-8')
cases_dict = yaml.safe_load(f)
print(cases_dict)

@allure.feature('Playwright_BDD_Framework_Demo')
class Test_class:

    def run_step(self, func, values):
        """
        :param func:
        :param values:
        :return:
        """
        func(*values)

    def run_case(self, POCcase):
        allure.dynamic.title(POCcase['title'])
        allure.dynamic.description(POCcase['des'])
        # 获取所有测试用例
        cases = POCcase['cases']
        try:
            for case in cases:
                func = self.page.__getattribute__(case['method'])
                # 获取参数
                print("case_value:::", case.values())
                case_list = list(case.values())
                with allure.step(case['name']):
                    self.run_step(func, case_list[2:])
        except Exception:
            allure.attach(self.page.screenshot(), 'test case error screenshot', allure.attachment_type.PNG)
            pytest.fail('执行失败')
        allure.attach(self.page.screenshot(), 'test case success screenshot', allure.attachment_type.PNG)

    def setup_class(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    @allure.story('登录')
    @pytest.mark.parametrize('POCcases', cases_dict['loginpage'])
    def test_login(self, POCcases):
        self.run_case(POCcases)
        self.page.wait_for_timeout(3000)

    def teardown_class(self):
        self.browser.close()
        self.playwright.stop()
