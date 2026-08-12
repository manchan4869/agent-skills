# 高德地图路径规划 2.0 API（v5）

## 服务概述

路径规划 2.0（v5）是 v1 的升级版：参数统一为下划线风格，用 `show_fields` 机制控制可选返回字段，驾车策略枚举与 v1 不同。新增电动车路线规划。

- **服务标识**: `route_planning_v2`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/newroute>

## 各出行方式 API 端点

| 路线类型 | API 端点 | 说明 |
|---------|---------|------|
| walking 步行 | `https://restapi.amap.com/v5/direction/walking` | 支持备选路线 |
| driving 驾车 | `https://restapi.amap.com/v5/direction/driving` | 参数过长时用 POST |
| bicycling 骑行 | `https://restapi.amap.com/v5/direction/bicycling` | |
| electrobike 电动车 | `https://restapi.amap.com/v5/direction/electrobike` | v2 独有 |
| transit 公交 | `https://restapi.amap.com/v5/direction/transit/integrated` | |

**通用参数：** `key`（必填）、`output`（仅支持 JSON）、`callback`、`sig`

## 1. 驾车路线规划

**GET/POST** `https://restapi.amap.com/v5/direction/driving`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| origin | string | T | - | 起点坐标 `经度,纬度` |
| destination | string | T | - | 终点坐标 |
| origin_id / destination_id | string | | - | 起/终点 POI id，提升精度 |
| strategy | number | | 32 | 驾车策略：0 速度优先，1 费用优先，2 常规最快，32 高德推荐（默认），33 躲避拥堵，34 高速优先，35 不走高速，36 少收费，37 大路优先，38 速度最快，39-45 为组合策略 |
| waypoints | string | | - | 途经点，默认 1 个有序，最多 16 个 |
| avoidpolygons | string | | - | 避让区域，默认 1 个，最多 32 个 |
| plate | string | | - | 车牌（含省份全拼，如 京AHA322），判断限行 |
| cartype | number | | - | 0 燃油，1 纯电，2 插电混动 |
| ferry | number | | - | 0 用轮渡，1 不用 |
| show_fields | string | | - | 可选返回字段，逗号分隔：cost/tmcs/navi/cities/polyline |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v5/direction/driving" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.434307,39.90909" \
  --data-urlencode "destination=116.434446,39.90816" \
  --data-urlencode "strategy=33" \
  --data-urlencode "show_fields=cost,polyline" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- `route.paths[].distance`（米）、`restriction`（0 限行已规避/1 无法规避）
- `show_fields=cost` 返回 `cost.duration/tolls/toll_distance/toll_road/traffic_lights`
- `show_fields=tmcs` 返回实时路况 `tmcs[].tmc_status/tmc_distance/tmc_polyline`
- `show_fields=navi` 返回导航指引 `navi.action/assistant_action`
- `show_fields=cities` 返回途经城市 `cities[].adcode/citycode/city/district`
- `show_fields=polyline` 返回 `steps[].polyline` 坐标串

## 2. 步行路线规划

**GET** `https://restapi.amap.com/v5/direction/walking`

- 参数：`origin`、`destination`、`origin_id`、`destination_id`、`alternative_route`（1/2/3 条备选路线）、`show_fields`、`isindoor`（0 室外/1 室内算路）
- 响应：`route.paths[].distance/duration/steps[]`

## 3. 骑行 / 电动车路线规划

**GET** `https://restapi.amap.com/v5/direction/bicycling` / `.../electrobike`

- 参数：`origin`、`destination`、`show_fields`、`alternative_route`
- 响应：`route.paths[].distance/duration/steps[]`

## 4. 公交路线规划

**GET** `https://restapi.amap.com/v5/direction/transit/integrated`

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| origin / destination | string | T | 起/终点坐标 |
| originpoi / destinationpoi | string | | 起/终点 POI id，须成组传入 |
| city1 | string | T | 起点城市 citycode（如 010） |
| city2 | string | | 终点城市 citycode |
| ad1 / ad2 | string | | 起/终点 adcode |
| strategy | number | | 0 推荐，1 最经济，2 最少换乘，3 最少步行，4 最舒适，5 不乘地铁，6 地铁图，7 地铁优先，8 时间短 |
| AlternativeRoute | number | | 返回方案数 1-10，默认 5 |
| nightflag | number | | 是否计算夜班车 |
| date / time | string | | 出发日期/时间 |
| show_fields | string | | 可选返回字段 |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v5/direction/transit/integrated" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.466485,39.995197" \
  --data-urlencode "destination=116.46424,40.020642" \
  --data-urlencode "city1=010" \
  --data-urlencode "city2=010" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- `route.transits[].distance/nightflag/segments[]`（`walking`、`bus`、`railway`、`taxi` 分段）

## 常见问题

**Q: v2 和 v1 怎么选？**

A: 新项目推荐 v2（v5）：参数规范、策略更细、有电动车规划。v1（v3）为传统接口，骑行用 v4 端点。两者响应结构不同（v2 用 show_fields，v1 用 extensions=all）。

**Q: 驾车 strategy 与 v1 的区别？**

A: v1 策略 0-20，v2 策略 0-45（默认 32 高德推荐），枚举含义不同，切换版本时注意。

**Q: 车牌限行参数差异？**

A: v2 用 `plate`（如 京AHA322，含省份全拼）；v1 用 `province`+`number` 拆分。
