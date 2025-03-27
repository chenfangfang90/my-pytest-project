import pytest
from common.conftest import api_data  # 使用绝对路径导入


@pytest.fixture(scope="function")
def testcase_data(request):
    testcases_name = request.function.__name__
    return api_data.get(testcases_name)
