from core.result_base import ResultBase
from api.user import user
from common.logger import logger
from common.sign_utils import generate_request_header


def login_user(login, password):
    """
    登录用户
    :param login: 用户名
    :param password: 密码
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()
    payload = {
        "usrLogin": login,
        "password": password
    }
    # 生成带签名的请求头
    header = generate_request_header(
        method="POST",
        path="/ucmlUser/login",
        form_params=payload,
        is_json=True  # 根据接口需求设置
    )
    res = user.login(json=payload, headers=header)
    logger.info('登录接口返回数据：{}'.format(res.json()))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
        result.token = res.json()["data"]["token"]
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("登录用户 ==>> 返回结果 ==>> {}".format(result.response.text))
    return result


def get_check_project_list(project_type):
    """
   获取验车项目列表
    :param project_type:验车项目类型
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()
    res = user.get_car_check_project_list(project_type)
    logger.info(' 获取验车项目列表：{}'.format(res.json()))
    result.success = False
    if res.json()["code"] == 0:
        result.success = True
        result.data = res.json()["data"]
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
    result.msg = res.json()["msg"]
    result.response = res
    logger.info("：验车项目类型：{} ==>> 获取验车项目列表返回结果 ==>> {}".format(project_type, result.response.text))
    return result
