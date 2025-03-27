# testcases/test_get_car_check_project_list.py

import pytest
import allure
from operation.user import get_check_project_list
from common.conftest import api_data
from common.logger import logger


@allure.step('步骤1===>> 获取验车数据，验车类型={project_type}')
def step_1(project_type):
    # 这里可以添加更多步骤细节
    logger.info('步骤1==>> 验车类型:{}'.format(project_type))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic('针对单个接口测试')
@allure.feature('获取验车项目列表')
class TestGetCarCheckProjectList:
    @allure.story('用例--获取验车项目列表')
    @allure.description("""
    该用例是针对验车项目列表测试 
    验车项目类型：不填或为空查全部, 
    0.手动输入,
    1.车辆外观,
    2.车辆内饰和随车物品,
    3.车辆性能,
    4.增值小物件; 
    多个可以用,隔开(例：1,2,3)
    """)
    @allure.title(
        '测试数据：【参数类型： {project_type}，返回状态：{except_result}，返回code：{except_code}，返回msg:{except_msg}】')
    @pytest.mark.single
    @pytest.mark.parametrize("project_type, except_result, except_code, except_msg",
                             api_data["test_get_car_check_project_list"])
    def test_get_car_check_project_list(self, project_type, except_result, except_code, except_msg):
        logger.info('##################### 开始执行用例 #################')

        # 执行接口调用
        with allure.step("调用接口获取验车项目列表"):
            result = get_check_project_list(project_type)
            step_1(project_type)  # 嵌套步骤

            # 附加响应结果到Allure报告
            allure.attach(
                name="接口响应结果",
                body=str(result.response.json()),
                attachment_type=allure.attachment_type.JSON
            )

            logger.debug("接口响应内容：{}".format(result.response.text))

        # 添加断言步骤
        with allure.step("验证接口响应"):
            assert result.success == except_result, f"实际结果与预期不符: {result.error}"
            assert result.response.status_code == 200, "HTTP状态码异常"

            # 附加详细断言信息
            actual_code = result.response.json().get("code")
            allure.attach(
                f"预期状态码: {except_code}\n实际状态码: {actual_code}",
                name="状态码验证",
                attachment_type=allure.attachment_type.TEXT
            )
            assert actual_code == except_code, "状态码不匹配"
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-s", "--alluredir=./report"])
