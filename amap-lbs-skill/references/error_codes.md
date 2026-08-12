# 高德地图错误码与对照表

## 服务概述

Web 服务 API 通用 `infocode`/`info` 状态对照，以及天气查询的天气现象/风力/风向枚举对照，附请求排错流程。

- **官方文档**: <https://lbs.amap.com/api/webservice/guide/tools/info>（错误码）、<https://lbs.amap.com/api/webservice/guide/tools/weather-code>（天气对照）

## 请求排错流程

接口异常时按此顺序排查：

1. **对照错误码表**（下文）查询原因与解决方案
2. **检查 urlencode**：请求串在 Chrome 正常但 IE/服务器返回空，通常是参数未 urlencode；**批量模式下 `|` 分隔符不能一起转义**，否则报错
3. **检查配额**：日超限（10003）/频率超限（10004）等，详见下文
4. 仍未解决则提工单，需提供：Key、完整请求串、请求时间（精确到秒）、返回的错误信息、响应 Header（建议）

**访问超时排查**：
- 先确认是**链接超时**（多为自身网络环境问题）还是**响应超时**（需提供完整请求串+请求时间点）
- 所有接口都超时 → 极大可能是网络问题；单个接口超时 → 排除网络后提工单

**配额提升**：提工单选择"调升企业配额"，需提供业务场景、使用的接口路径、要调整的 Key、期望日配额、QPS 峰值与时段分布。高德评估后联系。

**重要禁忌**：**严禁对接口做压力测试**，系统会立即识别并自动封停服务，损失自负。

## 错误码对照表

请求正常返回 `status=1, infocode=10000`。失败时据此排查。

### 鉴权与权限（100xx）

| infocode | info | 含义 | 排查 |
|----------|------|------|------|
| 10000 | OK | 请求正常 | - |
| 10001 | INVALID_USER_KEY | key 不正确或过期 | 检查 key |
| 10002 | SERVICE_NOT_AVAILABLE | 无权限使用服务/路径拼写错误 | 检查服务权限、URL（如 v3/ip 误写 vv3/ip） |
| 10003 | DAILY_QUERY_OVER_LIMIT | 日访问量超限 | 次日 0 点自动恢复 |
| 10004 | ACCESS_TOO_FREQUENT | 1 分钟内访问过于频繁 | 下一分钟恢复 |
| 10005 | INVALID_USER_IP | 请求 IP 不在白名单 | 控制台配置白名单 |
| 10006 | INVALID_USER_DOMAIN | 绑定域名无效 | 控制台重新设置 |
| 10007 | INVALID_USER_SIGNATURE | 数字签名未通过 | 按指定算法生成签名 |
| 10008 | INVALID_USER_SCODE | MD5 安全码未通过 | 检查 key 绑定 |
| 10009 | USERKEY_PLAT_NOMATCH | key 与绑定平台不符 | 如用 JS key 调 Web 服务 |
| 10010 | IP_QUERY_OVER_LIMIT | 单 IP 请求超限 | 封停不自动恢复，需提工单 |
| 10012 | INSUFFICIENT_PRIVILEGES | 权限不足，服务被拒绝 | 商务申请 |
| 10013 | USER_KEY_RECYCLED | Key 被删除 | - |
| 10026 | INVALID_REQUEST | 账号被封禁 | 违规封禁可申诉 |
| 10041 | NO_EFFECTIVE_INTERFACE | 接口权限过期 | 提工单 |
| 10044 | USER_DAILY_QUERY_OVER_LIMIT | 账号维度日调用量超限 | 阈值内正常返回 |

### 参数与请求（2xxxx）

| infocode | info | 含义 |
|----------|------|------|
| 20000 | INVALID_PARAMS | 请求参数非法 |
| 20001 | MISSING_REQUIRED_PARAMS | 缺少必填参数 |
| 20002 | ILLEGAL_REQUEST | 请求协议非法（如应 GET 却用 POST） |
| 20003 | UNKNOWN_ERROR | 其他未知错误 |
| 20011 | INSUFFICIENT_ABROAD_PRIVILEGES | 坐标/规划点在海外但无海外权限 |
| 20012 | ILLEGAL_CONTENT | 查询信息存在非法内容 |
| 20800 | OUT_OF_SERVICE | 规划点不在中国大陆范围（路径规划） |
| 20801 | NO_ROADS_NEARBY | 规划点附近搜不到路（路径规划） |
| 20802 | ROUTE_FAIL | 路线计算失败（道路连通关系） |
| 20803 | OVER_DIRECTION_RANGE | 起点终点距离过长（路径规划） |

### 其他（4xxxx / 3xx）

| infocode | info | 含义 |
|----------|------|------|
| 300** | ENGINE_RESPONSE_DATA_ERROR | 服务响应失败，检查参数否则提工单 |
| 40000 | QUOTA_PLAN_RUN_OUT | 余额耗尽 |
| 40002 | SERVICE_EXPIRED | 购买服务到期 |
| 40003 | ABROAD_QUOTA_PLAN_RUN_OUT | 海外服务余额耗尽 |

> QPS/配额实时数据以控制台「流量分析-配额管理」为准（https://console.amap.com/dev/flow/manage）

## 天气对照表

### 天气现象

晴、少云、晴间多云、多云、阴、有风、平静、微风、和风、清风、强风/劲风、疾风、大风、烈风、风暴、狂爆风、飓风、热带风暴；霾/中度霾/重度霾/严重霾；阵雨、雷阵雨、雷阵雨并伴有冰雹、小雨、中雨、大雨、暴雨、大暴雨、特大暴雨、强阵雨、强雷阵雨、极端降雨；毛毛雨/细雨、雨、小雨-中雨、中雨-大雨、大雨-暴雨、暴雨-大暴雨、大暴雨-特大暴雨；雨雪天气、雨夹雪、阵雨夹雪、冻雨、雪、阵雪、小雪、中雪、大雪、暴雪、小雪-中雪、中雪-大雪、大雪-暴雪；浮尘、扬沙、沙尘暴、强沙尘暴、龙卷风、雾、浓雾、强浓雾、轻雾、大雾、特强浓雾；热、冷、未知

### 风力等级

≤3、4、5、6、7、8、9、10、11、12

### 风向

无风向、东北、东、东南、南、西南、西、西北、北、旋转不定
