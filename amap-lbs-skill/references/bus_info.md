# 高德地图公交信息查询 API

## 服务概述

查询公交站点与公交线路信息。**高级服务接口**，个人/企业认证用户有每日体验配额，超出需商务咨询。

- **服务标识**: `bus_info`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api-advanced/bus-inquiry>

## 四个子接口

| 接口 | 端点 | 用途 |
|------|------|------|
| 公交站 ID | `GET https://restapi.amap.com/v3/bus/stopid` | 按站 id 查站点 |
| 公交站关键字 | `GET https://restapi.amap.com/v3/bus/stopname` | 按名称查站点 |
| 公交路线 ID | `GET https://restapi.amap.com/v3/bus/lineid` | 按线路 id 查线路详情 |
| 公交路线关键字 | `GET https://restapi.amap.com/v3/bus/linename` | 按名称查线路 |

## 输入参数

**stopid：**
| 参数名 | 必填 | 说明 |
|--------|------|------|
| key | T | 高德 Web 服务 Key |
| id | T | 公交站 id |
| output | | JSON/XML |

**stopname：**
| 参数名 | 必填 | 说明 |
|--------|------|------|
| key | T | 高德 Web 服务 Key |
| keywords | T | 站点关键词（仅 1 个） |
| city | | adcode/citycode |
| offset | | 每页条数（≤100，默认 20） |
| page | | 页码（默认 1） |

**lineid：**
| 参数名 | 必填 | 说明 |
|--------|------|------|
| key | T | 高德 Web 服务 Key |
| id | T | 公交线路 id |
| extensions | | `base` 基本信息；`all` 含途径站与首末班时间 |

**linename：**
| 参数名 | 必填 | 说明 |
|--------|------|------|
| key | T | 高德 Web 服务 Key |
| keywords | T | 线路关键词（仅 1 个，如 451） |
| city | T | 城市名/citycode/adcode |
| extensions | | `base` 或 `all`（途径站/首末班） |
| offset | | 每页条数（默认 20） |
| page | | 页码（默认 1） |

## 请求示例

```bash
# 按线路名查线路（含途径站）
curl -s --get "https://restapi.amap.com/v3/bus/linename" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=451" \
  --data-urlencode "city=110000" \
  --data-urlencode "extensions=all" \
  --data-urlencode "appname=amap-lbs-skill"

# 按站点 id 查站点
curl -s --get "https://restapi.amap.com/v3/bus/stopid" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "id=BV10006672" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

- **站点**：`busstops[]` → `id/name/location/adcode/citycode/buslines[]`（途径线路：`id/location/name/start_stop/end_stop`）
- **线路**：`buslines[]` → `id/type/name/polyline/start_stop/end_stop/start_time/end_time/timedesc/distance/loop/status/direc/company/basic_price/total_price/bounds/busstops[]`（`id/name/location/sequence`）
- `extensions=all` 的线路详情含全部途经站（busstops）与首末班时间
- `timedesc` 为 JSON 字符串需自行解码

## 注意事项

- 四个子接口共用 `/v3/bus/` 前缀，靠路径区分
- `extensions=all` 仅在 lineid/linename 有意义
