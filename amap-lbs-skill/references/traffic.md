# 高德地图交通信息 API

## 服务概述

交通事件（事故/拥堵/施工）查询与实时路况态势查询。**两者均为商业授权接口，需商务工单开通，普通 key 无权限。**

- **交通事件文档**: <https://lbs.amap.com/api/webservice/guide/api/traffic-incident>
- **交通态势文档**: <https://lbs.amap.com/api/webservice/guide/api-advanced/traffic-situation-inquiry>

---

## 一、交通事件查询

**GET** `https://et-api.amap.com/event/queryByAdcode`（http，**不支持 JSONP/callback**）

> 注意：域名是 `et-api.amap.com`（非 restapi）。商业化接口，需城市/区域授权，有日访问量与 QPS 限制。

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| adcode | string | T | 授权城市 ADCODE（城市级） |
| clientKey | string | T | Web 服务 API 类型 Key |
| timestamp | number | T | 秒级时间戳 |
| digest | string | T | 鉴权动态密钥（根据授权密钥计算） |
| eventType | string | T | 事件类型，多个用 `;` 分隔（如 201 事故） |
| isExpressway | number | T | 1 仅高速，0 全部 |

### 响应解析

- `code` + `msg`（0 成功）；`data[]`：`eventID/eventType/roadName/brief/eventDesc/startTime/endTime/expressway/lines/x/y/source` 等
- 支持全国 360+ 城市，更新频率 2 分钟

---

## 二、交通态势查询

三种查询方式（响应结构相同，仅请求几何参数不同）：

| 方式 | 端点 | 必填参数 |
|------|------|---------|
| 指定线路 | `https://restapi.amap.com/v3/traffic/status/road` | `name`（道路名）+ `city` 或 `adcode`（二选一） |
| 圆形区域 | `https://restapi.amap.com/v3/traffic/status/circle` | `location`（中心点）+ `radius`（米，最大 4999，默认 1000） |
| 矩形区域 | `https://restapi.amap.com/v3/traffic/status/rectangle` | `rectangle`（左下右上顶点 `x1,y1;x2,y2`，对角线 ≤10km） |

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| key | string | T | 高德 Web 服务 Key |
| level | number | T | 路况等级：1 高速、2 城市快速路/国道、3 高速辅路、4 主要道路、5 一般道路、6 无名道路（含包含关系） |
| extensions | string | | `base` 概要，`all` 详细（含 roads） |
| output | string | | JSON/XML |

### 请求示例

```bash
# 指定道路
curl -s --get "https://restapi.amap.com/v3/traffic/status/road" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "name=北环大道" \
  --data-urlencode "adcode=440300" \
  --data-urlencode "level=4" \
  --data-urlencode "appname=amap-lbs-skill"

# 圆形区域
curl -s --get "https://restapi.amap.com/v3/traffic/status/circle" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.3057764,39.98641364" \
  --data-urlencode "radius=1500" \
  --data-urlencode "level=4" \
  --data-urlencode "extensions=all" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- `trafficinfo.description/evaluation`：区域路况综述
- `trafficinfo.expedite/congested/blocked/unknown`：畅通/缓行/拥堵/未知占比
- `trafficinfo.roads[]`（extensions=all）：`name/status/direction/lcodes/speed/polyline`
- 路况 `status` 枚举：0 未知，1 畅通，2 缓行，3 拥堵

## 注意事项

- 仅支持约 41 个城市（北京/上海/深圳/广州/杭州等）
- 高级服务接口，需商务咨询开通

## 常见问题

**Q: 交通态势 API 为什么会报 20003（UNKNOWN_ERROR）？**

A: 交通态势 API 并未覆盖所有路段，仅支持部分城市的部分路线，无法查询的路段会报错或返回无结果。换个支持城市/路段再试。

**Q: 实时路况如何获取？**

A: 用交通态势接口（`/v3/traffic/status/*`），支持按道路、圆形区域、矩形区域三种方式查询。
