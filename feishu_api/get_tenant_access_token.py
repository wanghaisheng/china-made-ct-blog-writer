import json

import lark_oapi as lark
from lark_oapi.api.auth.v3 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def get_access_token():
    # 创建client
    client = lark.Client.builder() \
        .app_id("YOUR_APP_ID") \
        .app_secret("YOUR_APP_SECRET") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: InternalTenantAccessTokenRequest = InternalTenantAccessTokenRequest.builder() \
        .request_body(InternalTenantAccessTokenRequestBody.builder()
            .app_id("cli_a796f4ed0428900b")
            .app_secret("wqv1hLh4or8q1tBBZ2ks7bEywyVUtLq3")
            .build()) \
        .build()

    # 发起请求
    response: InternalTenantAccessTokenResponse = client.auth.v3.tenant_access_token.internal(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.auth.v3.tenant_access_token.internal failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response, indent=4))
    res = lark.JSON.marshal(response, indent=4)
    print(type(res)) # 显示是字符串
    # 将返回内容解析为字典
    res_dict = json.loads(res)
    content_str = res_dict['raw']['content'] # 获取 content 项字符串
    content_dict = json.loads(content_str)  # 将 content 字符串解析成字典
    tenant_access_token = content_dict['tenant_access_token']
    
    return tenant_access_token