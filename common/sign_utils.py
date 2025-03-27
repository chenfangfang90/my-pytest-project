# test_utils/sign_utils.py
import hmac
import hashlib
import base64
import time
import random
import string
import os
from common.read_data import data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
kNetworkGatewayAPPKey = data.load_ini(data_file_path)["host"]["kNetworkGatewayAPPKey"]
kNetworkGatewayAPPSECRET = data.load_ini(data_file_path)["host"]["kNetworkGatewayAPPSECRET"]

CLOUDAPI_LF = '\n'
CLOUDAPI_CA_HEADER_PREFIX = "X-Ca-"
CLOUDAPI_CONTENT_TYPE_JSON = "application/x-www-form-urlencoded; charset=UTF-8"
ACCEPT_CONTENT_TYPE_JSON = "application/json; charset=UTF-8"
CLOUDAPI_CONTENT_TYPE_FORM = "application/x-www-form-urlencoded; charset=UTF-8"


def hmac_sha256(key: str, data: str) -> str:
    signature = hmac.new(
        key.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()


def build_resource(path: str, query_params: dict, form_params: dict) -> str:
    merged_params = {}
    merged_params.update(query_params)
    merged_params.update(form_params)
    sorted_params = sorted(merged_params.items(), key=lambda x: x[0])
    param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
    return f"{path}?{param_str}" if param_str else path


def build_headers(headers: dict) -> str:
    ca_headers = {}
    for k in headers:
        if k.startswith(CLOUDAPI_CA_HEADER_PREFIX):
            ca_headers[k] = headers[k]

    sorted_headers = sorted(ca_headers.items(), key=lambda x: x[0])
    header_str = CLOUDAPI_LF.join([f"{k}:{v}" for k, v in sorted_headers]) + CLOUDAPI_LF
    signature_headers = ','.join([k for k, _ in sorted_headers])

    headers['X-Ca-Signature-Headers'] = signature_headers
    return header_str


def build_string_to_sign(method: str, headers: dict, path: str, query_params: dict, form_params: dict) -> str:
    parts = [
        method,
        headers.get("Accept", ""),
        headers.get("Content-MD5", ""),
        headers.get("Content-Type", ""),
        headers.get("Date", ""),
        build_headers(headers.copy()),
        build_resource(path, query_params, form_params)
    ]
    return CLOUDAPI_LF.join(parts)


def sign(method: str, headers: dict, path: str, query_params: dict, form_params: dict, app_secret: str) -> str:
    string_to_sign = build_string_to_sign(method, headers, path, query_params, form_params)
    return hmac_sha256(app_secret, string_to_sign)


def generate_request_header(
        method: str,
        path: str,
        query_params: dict = None,
        form_params: dict = None,
        app_key: str = kNetworkGatewayAPPKey,
        app_secret: str = kNetworkGatewayAPPSECRET,
        is_json: bool = False
) -> dict:
    if query_params is None:
        query_params = {}
    if form_params is None:
        form_params = {}

    content_type = CLOUDAPI_CONTENT_TYPE_JSON if is_json else CLOUDAPI_CONTENT_TYPE_FORM
    headers = {
        "Content-Type": content_type,
        "Accept": ACCEPT_CONTENT_TYPE_JSON,
        "X-Ca-Key": app_key,
        "X-Ca-Timestamp": str(int(time.time() * 1000)),
        "X-Ca-Nonce": ''.join(random.choices(string.ascii_letters + string.digits, k=15)),
        "X-Ca-Version": "1"
    }

    signature = sign(
        method=method.upper(),
        headers=headers,
        path=path,
        query_params=query_params,
        form_params=form_params,
        app_secret=app_secret
    )
    headers["X-Ca-Signature"] = signature
    return headers
